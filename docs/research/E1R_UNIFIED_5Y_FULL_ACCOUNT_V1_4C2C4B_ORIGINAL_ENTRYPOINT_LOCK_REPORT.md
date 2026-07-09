# E1R Combined 5Y — 4C-2C-4B Original Entrypoint Lock

Generated At: `2026-07-09T12:59:43.645670+00:00`

## Policy
```json
{
  "strategy_logic_changed": false,
  "backtest_run": false,
  "dashboard_changed": false,
  "purpose": "Lock original executable entrypoints before 5Y combined rerun."
}
```

## Function Signatures
```json
[
  {
    "module": "src.engine.e1r_composer",
    "import_ok": true,
    "functions": [
      {
        "name": "compose_e1r_v0_2_variant",
        "exists": true,
        "signature": "(core_variant_result: 'dict[str, Any]', sidecar_result: 'dict[str, Any]', initial_equity: 'float' = 100000.0) -> 'dict[str, Any]'"
      },
      {
        "name": "extract_core_interval_returns",
        "exists": true,
        "signature": "(core_daily_equity_records: 'Sequence[dict[str, Any]]', sidecar_records: 'Sequence[dict[str, Any]]') -> 'list[dict[str, Any]]'"
      },
      {
        "name": "build_equity_records_from_returns",
        "exists": true,
        "signature": "(interval_records: 'Sequence[dict[str, Any]]', initial_equity: 'float') -> 'list[dict[str, Any]]'"
      }
    ]
  },
  {
    "module": "src.engine.e1r_sidecar_sleeve",
    "import_ok": true,
    "functions": [
      {
        "name": "build_e1r_sidecar_sleeve",
        "exists": true,
        "signature": "(stock_dir: 'Path', spx_path: 'Path', regime_path: 'Path', config: 'E1RSidecarConfig') -> 'dict[str, Any]'"
      }
    ]
  },
  {
    "module": "src.engine.backtest",
    "import_ok": true,
    "functions": [
      {
        "name": "run_stateful_simulation",
        "exists": true,
        "signature": "(symbols: 'list[str]', prices_map: 'dict[str, list[float]]', dates_map: 'dict[str, list[str]]', spx_prices: 'list[float]', spx_dates: 'list[str]', ohlc_map: 'dict' = None, assumptions: 'dict' = None, step: 'int' = 1, min_history: 'int' = 120, market_score_default: 'float' = 60.0, sim_start_date: 'str' = None, sim_end_date: 'str' = None, ndx_prices: 'list' = None, ndx_dates: 'list' = None, sox_prices: 'list' = None, sox_dates: 'list' = None, vix_prices: 'list' = None, vix_dates: 'list' = None) -> 'dict'"
      }
    ]
  }
]
```

## Locked Entrypoints
```json
{
  "uptrend_candidate_entrypoint": {
    "status": "LOCKED_IF_COMPOSER_CONTRACT_CONFIRMS",
    "module": "src.engine.e1r_composer",
    "function": "compose_e1r_v0_2_variant",
    "reason": "This is the recovered E1R composer entrypoint; must be verified to preserve original UPTREND branch, not replaced."
  },
  "sideways_sidecar_entrypoint": {
    "status": "LOCKED_IF_SIDECAR_CONTRACT_CONFIRMS",
    "module": "src.engine.e1r_sidecar_sleeve",
    "function": "build_e1r_sidecar_sleeve",
    "reason": "This is the recovered sidecar sleeve builder; must be used as original SIDEWAYS/MA_CONFLICT source, with Top10 as candidate pool only."
  },
  "full_account_engine": {
    "status": "AVAILABLE_BUT_REQUIRES_ADAPTER_GUARD",
    "module": "src.engine.backtest",
    "function": "run_stateful_simulation",
    "reason": "Prior 4C-2C full run used this engine but violated max holdings. Any adapter must enforce account holdings <=3 and must not alter strategy rules."
  }
}
```

## Validation Questions Before Rerun
```json
[
  {
    "topic": "UPTREND",
    "must_confirm": "compose_e1r_v0_2_variant contains original UPTREND branch, especially E1R_UPTREND_CONFIRMED, without newly invented entry/exit logic."
  },
  {
    "topic": "SIDEWAYS / MA_CONFLICT",
    "must_confirm": "build_e1r_sidecar_sleeve is the original validated sidecar source; selected_count_max/Top10 remains candidate pool, not live holdings."
  },
  {
    "topic": "DETERIORATION / RECOVERY",
    "must_confirm": "Whether original sidecar included only MA_CONFLICT or also DETERIORATION/RECOVERY. If not proven, keep DETERIORATION/RECOVERY cash/defensive."
  },
  {
    "topic": "DOWNTREND",
    "must_confirm": "No normal buy execution. Cash/defensive only."
  },
  {
    "topic": "Global account cap",
    "must_confirm": "Adapter/engine output open_positions_count never exceeds 3."
  }
]
```

## AST Functions
```json
[
  {
    "path": "src/engine/e1r_composer.py",
    "function": "extract_core_interval_returns",
    "line": 94,
    "matched_keywords": [
      "gross_exposure"
    ],
    "args": [
      "core_daily_equity_records",
      "sidecar_records"
    ],
    "source_head": "def extract_core_interval_returns(\n    core_daily_equity_records: Sequence[dict[str, Any]],\n    sidecar_records: Sequence[dict[str, Any]],\n) -> list[dict[str, Any]]:\n    \"\"\"\n    Align core daily returns to sidecar intervals by next_date.\n\n    Returns one record per shared interval:\n    {\n      date,\n      next_date,\n      core_return,\n      sidecar_return,\n      spx_return,\n      ...\n    }\n    \"\"\"\n    core_by_end_date = {}\n\n    for row in core_daily_equity_records:\n        date = row.get(\"date\")\n        if not date:\n            continue\n\n        r = safe_float(row.get(\"daily_return\"))\n        if r is None:\n            # Some historical outputs may store pct instead of decimal.\n            rp = safe_float(row.get(\"daily_return_pct\"))\n            r = None if rp is None else rp / 100.0\n\n        if r is None:\n            continue\n\n        core_by_end_date[date] = row | {\"_normalized_daily_return\": r}\n\n    aligned: list[dict[str, Any]] = []\n\n    for sidecar in sidecar_records:\n        date = sidecar.get(\"date\")\n        next_date = sidecar.get(\"next_date\")\n\n        if not date or not next_date:\n            continue\n\n        core = core_by_end_date.get(next_date)\n        if core is None:\n            continue\n\n        core_return = safe_float(core.get(\"_normalized_daily_return\")) or 0.0\n        sidecar_return = safe_float(sidecar.get(\"portfolio_return\")) or 0.0\n        spx_return = safe_float(sidecar.get(\"spx_return\")) or 0.0\n\n        combined_return = (1.0 + core_return) * (1.0 + sidecar_return) - 1.0\n\n        aligned.append({\n            \"date\": date,\n            \"next_date\": next_date,\n            \"core_end_date\": next_date,\n            \"core_return\": core_return,\n            \"core_return_pct\": pct_display(core_return),\n            \"sidecar_return\": sidecar_return,\n            \"sidecar_return_pct\": pct_display(sidecar_return),\n            \"combined_return\": combined_return,\n            \"combined_return_pct\": pct_display(combined_return),\n            \"spx_return\": spx_return,\n            \"spx_return_pct\": pct_display(spx_return),\n            \"regime\": sidecar.get(\"regime\"),\n            \"subclass\": sidecar.get(\"subclass\"),\n            \"sidecar_active\": bool(sidecar.get(\"is_active\")),\n            \"sidecar_selected_count\": sidecar.get(\"selected_count\"),\n            \"sidecar_gross_exposure\": sidecar.get(\"gross_exposure\"),\n            \"sidecar_holdings\": sidecar.get(\"holdings\", []),\n        })\n\n    return aligned"
  },
  {
    "path": "src/engine/e1r_composer.py",
    "function": "build_equity_records_from_returns",
    "line": 171,
    "matched_keywords": [
      "gross_exposure"
    ],
    "args": [
      "interval_records",
      "initial_equity"
    ],
    "source_head": "def build_equity_records_from_returns(\n    interval_records: Sequence[dict[str, Any]],\n    initial_equity: float,\n) -> list[dict[str, Any]]:\n    equity = initial_equity\n    peak = initial_equity\n    records: list[dict[str, Any]] = []\n\n    for row in interval_records:\n        r = safe_float(row.get(\"combined_return\")) or 0.0\n        equity *= 1.0 + r\n        peak = max(peak, equity)\n\n        drawdown = equity / peak - 1.0 if peak > 0 else 0.0\n\n        records.append({\n            \"date\": row[\"next_date\"],\n            \"interval_start_date\": row[\"date\"],\n            \"interval_end_date\": row[\"next_date\"],\n            \"total_equity\": equity,\n            \"equity\": equity,\n            \"daily_return\": r,\n            \"daily_return_pct\": pct_display(r),\n            \"drawdown\": drawdown,\n            \"drawdown_pct\": pct_display(drawdown),\n\n            \"core_return\": row[\"core_return\"],\n            \"core_return_pct\": row[\"core_return_pct\"],\n            \"sidecar_return\": row[\"sidecar_return\"],\n            \"sidecar_return_pct\": row[\"sidecar_return_pct\"],\n            \"spx_return\": row[\"spx_return\"],\n            \"spx_return_pct\": row[\"spx_return_pct\"],\n\n            \"spx_regime\": row.get(\"regime\"),\n            \"sideways_subclass\": row.get(\"subclass\"),\n            \"sidecar_active\": row.get(\"sidecar_active\"),\n            \"sidecar_selected_count\": row.get(\"sidecar_selected_count\"),\n            \"sidecar_gross_exposure\": row.get(\"sidecar_gross_exposure\"),\n        })\n\n    return records"
  },
  {
    "path": "src/engine/e1r_composer.py",
    "function": "compose_e1r_v0_2_variant",
    "line": 283,
    "matched_keywords": [
      "compose_e1r_v0_2_variant",
      "SIDEWAYS",
      "MA_CONFLICT",
      "gross_exposure"
    ],
    "args": [
      "core_variant_result",
      "sidecar_result",
      "initial_equity"
    ],
    "source_head": "def compose_e1r_v0_2_variant(\n    core_variant_result: dict[str, Any],\n    sidecar_result: dict[str, Any],\n    initial_equity: float = 100000.0,\n) -> dict[str, Any]:\n    core_records = core_variant_result.get(\"daily_equity_records\", [])\n    sidecar_records = sidecar_result.get(\"records\", [])\n\n    interval_records = extract_core_interval_returns(core_records, sidecar_records)\n    equity_records = build_equity_records_from_returns(interval_records, initial_equity)\n    summary = summarize_combined_variant(interval_records, equity_records, initial_equity)\n\n    result = copy.deepcopy(core_variant_result)\n\n    sidecar_summary = sidecar_result.get(\"summary\", {}) or {}\n\n    result.update({\n        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2\",\n        \"strategy_variant\": \"E1R_regime_aware_v0_2_formal_sidecar_sleeve\",\n        \"version\": \"E1R-v0.2-formal-sidecar-sleeve\",\n        \"research_status\": \"FORMAL_SIDECAR_SLEEVE_ENGINE\",\n        \"core_total_trades\": core_variant_result.get(\"total_trades\"),\n        \"sidecar_trade_count_approx\": sidecar_summary.get(\"trade_count_approx\"),\n        \"combined_trade_count_note\": (\n            \"total_trades remains inherited from E1R v0.1 core; \"\n            \"sidecar_trade_count_approx counts daily basket holdings and is not \"\n            \"stateful round-trip trade count.\"\n        ),\n        \"e1r_v0_2_composition\": {\n            \"core_variant\": \"E1R_REGIME_AWARE_V0_1\",\n            \"sidecar_engine\": sidecar_result.get(\"engine\"),\n            \"sidecar_version\": sidecar_result.get(\"version\"),\n            \"alignment\": \"core daily return ending at next_date aligned to sidecar date->next_date interval\",\n            \"composition_formula\": \"(1 + core_return) * (1 + sidecar_return) - 1\",\n            \"sidecar_config\": sidecar_result.get(\"config\", {}),\n            \"sidecar_sample\": sidecar_result.get(\"sample\", {}),\n            \"sidecar_summary\": sidecar_result.get(\"summary\", {}),\n            \"combined_summary\": summary,\n        },\n        \"daily_equity_records\": equity_records,\n        \"daily_equity_record_count\": len(equity_records),\n        \"e1r_v0_2_interval_records_sample\": {\n            \"first_5\": interval_records[:5],\n            \"last_5\": interval_records[-5:],\n        },\n    })\n\n    # Override summary-level fields with formal combined values.\n    for key in (\n        \"total_return_pct\",\n        \"spx_return_pct\",\n        \"alpha_pct\",\n        \"max_drawdown_pct\",\n        \"profit_factor\",\n        \"sharpe_ratio\",\n    ):\n        if key in summary:\n            result[key] = summary[key]\n\n    result[\"total_days\"] = summary[\"total_days\"]\n    result[\"sidecar_active_days\"] = summary[\"sidecar_active_days\"]\n    result[\"sidecar_active_by_regime\"] = summary[\"sidecar_active_by_regime\"]\n    result[\"sidecar_active_by_subclass\"] = summary[\"sidecar_active_by_subclass\"]\n    result[\"sidecar_simple_contribution_by_regime_pct\"] = summary[\"sidecar_simple_contribution_by_regime_pct\"]\n    result[\"sidecar_simple_contribution_by_subclass_pct\"] = summary[\"sidecar_simple_contribution_by_subclass_pct\"]\n\n    result.setdefault(\"strategy_controls\", {})\n    result[\"strategy_controls\"].update({\n        \"regime_aware_logic\": \"UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE\",\n        \"e1r_v0_2_formal_sidecar_sleeve\": True,\n        \"e1r_v0_2_core_variant\": \"E1R_REGIME_AWARE_V0_1\",\n        \"e1r_v0_2_sidecar_allowed_subclasses\": sidecar_result.get(\"config\", {}).get(\"allowed_subclasses\"),\n        \"e1r_v0_2_sidecar_top_n\": sidecar_result.get(\"config\", {}).get(\"top_n\"),\n        \"e1r_v0_2_sidecar_gross_exposure\": sidecar_result.get(\"config\", {}).get(\"gross_exposure\"),\n        \"e1r_v0_2_excluded_symbols\": sidecar_result.get(\"config\", {}).get(\"excluded_symbols\"),\n    })\n\n    return result"
  },
  {
    "path": "src/engine/e1r_sidecar_sleeve.py",
    "function": "build_daily_rankings",
    "line": 356,
    "matched_keywords": [
      "SIDEWAYS"
    ],
    "args": [
      "stocks",
      "spx",
      "regimes",
      "intervals",
      "config"
    ],
    "source_head": "def build_daily_rankings(\n    stocks: dict[str, dict[str, Any]],\n    spx: dict[str, Any],\n    regimes: dict[str, dict[str, Any]],\n    intervals: Sequence[tuple[str, str]],\n    config: E1RSidecarConfig,\n) -> dict[str, dict[str, Any]]:\n    rankings: dict[str, dict[str, Any]] = {}\n\n    for date, next_date in intervals:\n        regime_info = regimes.get(date, {})\n        if regime_info.get(\"regime\") != \"SIDEWAYS\":\n            continue\n\n        candidates: list[dict[str, Any]] = []\n\n        for asset in stocks.values():\n            if date not in asset[\"by_date\"] or next_date not in asset[\"by_date\"]:\n                continue\n\n            candidate = score_candidate(asset, spx, date, config)\n            if candidate is None:\n                continue\n\n            one_day_return = close_to_close_return(asset, date, next_date)\n            if one_day_return is None:\n                continue\n\n            candidate[\"one_day_return\"] = one_day_return\n            candidates.append(candidate)\n\n        candidates.sort(key=lambda x: x[\"score\"], reverse=True)\n\n        rankings[date] = {\n            \"date\": date,\n            \"next_date\": next_date,\n            \"regime\": \"SIDEWAYS\",\n            \"subclass\": regime_info.get(\"subclass\") or \"NO_SUBCLASS\",\n            \"candidate_count\": len(candidates),\n            \"candidates\": candidates,\n        }\n\n    return rankings"
  },
  {
    "path": "src/engine/e1r_sidecar_sleeve.py",
    "function": "run_daily_rebalanced_sidecar",
    "line": 401,
    "matched_keywords": [
      "SIDEWAYS",
      "gross_exposure"
    ],
    "args": [
      "rankings",
      "spx",
      "regimes",
      "intervals",
      "config"
    ],
    "source_head": "def run_daily_rebalanced_sidecar(\n    rankings: dict[str, dict[str, Any]],\n    spx: dict[str, Any],\n    regimes: dict[str, dict[str, Any]],\n    intervals: Sequence[tuple[str, str]],\n    config: E1RSidecarConfig,\n) -> list[dict[str, Any]]:\n    allowed_subclasses = set(config.allowed_subclasses)\n    top_n = int(config.top_n)\n    gross_exposure = float(config.gross_exposure)\n\n    records: list[dict[str, Any]] = []\n\n    for date, next_date in intervals:\n        regime_info = regimes.get(date, {})\n        regime = regime_info.get(\"regime\") or \"NO_REGIME\"\n        subclass = regime_info.get(\"subclass\") or \"NO_SUBCLASS\"\n\n        spx_return = close_to_close_return(spx, date, next_date) or 0.0\n\n        ranked = rankings.get(date, {})\n        candidates = ranked.get(\"candidates\", [])\n\n        is_active = (\n            regime == \"SIDEWAYS\"\n            and subclass in allowed_subclasses\n            and top_n > 0\n            and gross_exposure > 0\n            and bool(candidates)\n        )\n\n        holdings: list[dict[str, Any]] = []\n        portfolio_return = 0.0\n\n        if is_active:\n            selected = candidates[:top_n]\n            weight = gross_exposure / len(selected)\n\n            for candidate in selected:\n                raw_return = candidate[\"one_day_return\"]\n                contribution = weight * raw_return\n                portfolio_return += contribution\n\n                holdings.append({\n                    \"symbol\": candidate[\"symbol\"],\n                    \"score\": candidate[\"score\"],\n                    \"weight\": weight,\n                    \"raw_return\": raw_return,\n                    \"raw_return_pct\": pct_display(raw_return),\n                    \"weighted_contribution\": contribution,\n                    \"weighted_contribution_pct\": pct_display(contribution),\n                })\n\n        records.append({\n            \"date\": date,\n            \"next_date\": next_date,\n            \"regime\": regime,\n            \"subclass\": subclass,\n            \"is_active\": is_active,\n            \"candidate_count\": len(candidates),\n            \"selected_count\": len(holdings),\n            \"gross_exposure\": gross_exposure if is_active else 0.0,\n            \"portfolio_return\": portfolio_return,\n            \"portfolio_return_pct\": pct_display(portfolio_return),\n            \"spx_return\": spx_return,\n            \"spx_return_pct\": pct_display(spx_return),\n            \"holdings\": holdings,\n        })\n\n    return records"
  },
  {
    "path": "src/engine/e1r_sidecar_sleeve.py",
    "function": "summarize_sidecar",
    "line": 473,
    "matched_keywords": [
      "SIDEWAYS",
      "MA_CONFLICT",
      "gross_exposure"
    ],
    "args": [
      "records",
      "config"
    ],
    "source_head": "def summarize_sidecar(\n    records: Sequence[dict[str, Any]],\n    config: E1RSidecarConfig,\n) -> dict[str, Any]:\n    equity = config.initial_equity\n    equity_curve = [equity]\n\n    daily_returns = [r[\"portfolio_return\"] for r in records]\n    active_records = [r for r in records if r[\"is_active\"]]\n    active_returns = [r[\"portfolio_return\"] for r in active_records]\n    active_spx_returns = [r[\"spx_return\"] for r in active_records]\n\n    for record in records:\n        equity *= 1.0 + record[\"portfolio_return\"]\n        equity_curve.append(equity)\n\n    full_strategy_return = equity_curve[-1] / config.initial_equity - 1.0\n    full_spx_return = compound_return(r[\"spx_return\"] for r in records)\n    active_strategy_return = compound_return(active_returns)\n    active_spx_return = compound_return(active_spx_returns)\n\n    wins = [r for r in active_records if r[\"portfolio_return\"] > 0]\n    losses = [r for r in active_records if r[\"portfolio_return\"] < 0]\n\n    return {\n        \"name\": \"E1R_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE\",\n        \"allowed_subclasses\": list(config.allowed_subclasses),\n        \"top_n\": config.top_n,\n        \"gross_exposure\": config.gross_exposure,\n        \"excluded_symbols\": list(config.excluded_symbols),\n\n        \"total_days\": len(records),\n        \"active_days\": len(active_records),\n        \"exposure_pct_full_period\": (\n            100.0 * len(active_records) / len(records)\n            if records else None\n        ),\n\n        \"full_period_strategy_return_pct\": pct_display(full_strategy_return),\n        \"full_period_spx_return_pct\": pct_display(full_spx_return),\n        \"full_period_excess_vs_spx_pct\": pct_display(full_strategy_return - full_spx_return),\n\n        \"active_window_strategy_return_pct\": pct_display(active_strategy_return),\n        \"active_window_spx_return_pct\": pct_display(active_spx_return),\n        \"active_window_excess_vs_spx_pct\": pct_display(active_strategy_return - active_spx_return),\n\n        \"max_drawdown_pct\": pct_display(max_drawdown(equity_curve)),\n        \"profit_factor\": profit_factor(daily_returns),\n        \"sharpe\": sharpe_ratio(daily_returns),\n\n        \"active_day_win_rate_pct\": (\n            100.0 * len(wins) / len(active_records)\n            if active_records else None\n        ),\n        \"winning_active_days\": len(wins),\n        \"losing_active_days\": len(losses),\n        \"avg_active_day_return_pct\": pct_display(mean_or_none(active_returns)),\n        \"median_active_day_return_pct\": pct_display(median_or_none(active_returns)),\n\n        \"trade_count_approx\": sum(len(r[\"holdings\"]) for r in active_records),\n        \"equity_start\": config.initial_equity,\n        \"equity_end\": equity_curve[-1],\n    }"
  },
  {
    "path": "src/engine/e1r_sidecar_sleeve.py",
    "function": "build_e1r_sidecar_sleeve",
    "line": 538,
    "matched_keywords": [
      "build_e1r_sidecar_sleeve",
      "SIDEWAYS",
      "gross_exposure"
    ],
    "args": [
      "stock_dir",
      "spx_path",
      "regime_path",
      "config"
    ],
    "source_head": "def build_e1r_sidecar_sleeve(\n    stock_dir: Path,\n    spx_path: Path,\n    regime_path: Path,\n    config: E1RSidecarConfig,\n) -> dict[str, Any]:\n    spx = load_asset(spx_path)\n    regimes = load_regimes(regime_path)\n    stocks, excluded_found = load_stock_universe(stock_dir, config)\n\n    intervals = build_backtest_intervals(spx, regimes, config)\n    rankings = build_daily_rankings(stocks, spx, regimes, intervals, config)\n    records = run_daily_rebalanced_sidecar(rankings, spx, regimes, intervals, config)\n    summary = summarize_sidecar(records, config)\n\n    regime_counts: dict[str, int] = {}\n    subclass_counts: dict[str, int] = {}\n\n    for record in records:\n        regime = record[\"regime\"]\n        subclass = record[\"subclass\"]\n        regime_counts[regime] = regime_counts.get(regime, 0) + 1\n        if regime == \"SIDEWAYS\":\n            subclass_counts[subclass] = subclass_counts.get(subclass, 0) + 1\n\n    return {\n        \"engine\": \"e1r_sidecar_sleeve\",\n        \"version\": \"v0.2_formal_sleeve_engine\",\n        \"config\": {\n            \"start_date\": config.start_date,\n            \"end_date\": config.end_date,\n            \"allowed_subclasses\": list(config.allowed_subclasses),\n            \"top_n\": config.top_n,\n            \"gross_exposure\": config.gross_exposure,\n            \"min_history_days\": config.min_history_days,\n            \"min_price\": config.min_price,\n            \"initial_equity\": config.initial_equity,\n            \"excluded_symbols\": list(config.excluded_symbols),\n        },\n        \"sample\": {\n            \"intervals\": len(intervals),\n            \"first_interval\": {\n                \"date\": intervals[0][0],\n                \"next_date\": intervals[0][1],\n            } if intervals else None,\n            \"last_interval\": {\n                \"date\": intervals[-1][0],\n                \"next_date\": intervals[-1][1],\n            } if intervals else None,\n            \"stock_universe_after_exclusions\": len(stocks),\n            \"excluded_symbols_found_in_raw_data\": excluded_found,\n            \"regime_counts\": regime_counts,\n            \"sideways_subclass_counts\": subclass_counts,\n        },\n        \"summary\": summary,\n        \"records\": records,\n    }"
  },
  {
    "path": "src/engine/backtest.py",
    "function": "run_stateful_simulation",
    "line": 763,
    "matched_keywords": [
      "run_stateful_simulation",
      "E1R_UPTREND_CONFIRMED",
      "E1R_UPTREND_EMERGING",
      "SIDEWAYS",
      "DOWNTREND",
      "max_positions",
      "candidate_top_n",
      "entry_top_n",
      "open_positions_count"
    ],
    "args": [
      "symbols",
      "prices_map",
      "dates_map",
      "spx_prices",
      "spx_dates",
      "ohlc_map",
      "assumptions",
      "step",
      "min_history",
      "market_score_default",
      "sim_start_date",
      "sim_end_date",
      "ndx_prices",
      "ndx_dates",
      "sox_prices",
      "sox_dates",
      "vix_prices",
      "vix_dates"
    ],
    "source_head": "def run_stateful_simulation(\n    symbols:        list[str],\n    prices_map:     dict[str, list[float]],\n    dates_map:      dict[str, list[str]],\n    spx_prices:     list[float],\n    spx_dates:      list[str],\n    ohlc_map:       dict = None,\n    assumptions:    dict = None,\n    step:           int  = 1,\n    min_history:    int  = 120,\n    market_score_default: float = 60.0,\n    sim_start_date: str  = None,  # 交易执行起始日（None=从 min_history 后开始）\n    sim_end_date:   str  = None,  # 交易执行截止日（None=到末尾）\n    ndx_prices:     list = None,  # NDX 收盘价（Gate v2 Leadership 判断）\n    ndx_dates:      list = None,\n    sox_prices:     list = None,  # SOX 收盘价\n    sox_dates:      list = None,\n    vix_prices:     list = None,  # VIX 收盘价\n    vix_dates:      list = None,\n) -> dict:\n    \"\"\"\n    Layer D v1.6: Strict Top3 + RS threshold + MinHold + Relative SPX Stop\n\n    修正项（相比 v3）：\n    1. SPX master calendar — 时间轴以 SPX dates 为准\n    2. Date-based alignment — 所有股票按日期查找，不用 index 直接对齐\n    3. skipped_orders_by_reason — 跳过原因分类统计\n    4. sample_validity 检查 — 样本不足时返回 INSUFFICIENT_SAMPLE\n    \"\"\"\n    logger.info(\"[Backtest Layer D v1.6] Strict Top3 + RS/MinHold/RelStop Backtest...\")\n\n    # ── 冻结参数 ─────────────────────────────────────────\n    a        = assumptions or LAYER_D_ASSUMPTIONS\n    max_pos  = a[\"max_positions\"]\n    buy_pct  = a[\"buy_size\"]  / max_pos       # Top3: 1/3 per full slot\n    add_pct  = a[\"add_size\"]  / max_pos       # Top3: +1/6, only useful after REDUCE\n    max_pct  = a[\"max_single_size\"] / max_pos # Top3: max 1/3 per position\n    one_way  = a[\"total_one_way\"]             # 0.001\n    init_cap = float(a.get(\"initial_capital\", 100_000))\n    strategy_variant = a.get(\"strategy_variant\", \"top3_entry_rs_minhold_relstop\")\n    e1r_shell_mode = bool(a.get(\"e1r_shell_mode\", False))\n    e1r_regime_wiring_enabled = bool(a.get(\"e1r_regime_wiring_enabled\", False))\n    e1r_uptrend_execution_enabled = bool(a.get(\"e1r_uptrend_execution_enabled\", False))\n    e1r_regime_daily = a.get(\"e1r_regime_daily\", {}) or {}\n\n    def _e1r_regime_on(date: str) -> str:\n        if not e1r_regime_wiring_enabled or not date:\n            return \"N/A\"\n        rec = e1r_regime_daily.get(date, {})\n        if isinstance(rec, dict):\n            return rec.get(\"regime\") or rec.get(\"spx_regime\") or rec.get(\"weekly_regime\") or \"UNCLASSIFIED\"\n        if isinstance(rec, str):\n            return rec\n        return \"UNCLASSIFIED\"\n\n    def _e1r_mode_for_regime(regime: str) -> str:\n        if regime == \"UPTREND\":\n            return \"UPTREND_EMERGING_CONFIRMED_ENABLED\"\n        if regime == \"SIDEWAYS\":\n            return \"SIDEWAYS_QUALITY_BREAKOUT_ONLY\"\n        if regime == \"DOWNTREND\":\n            return \"DOWNTREND_EXCEPTION_ONLY\"\n        if regime == \"N/A\":\n            return \"N/A\"\n        return \"UNCLASSIFIED_NO_RISK_EXPANSION\"\n\n    def _e1r_risk_budget_for_regime(regime: str) -> dict:\n        if regime == \"UPTREND\":\n            return {\"mode\": \"UPTREND_RISK_ON\", \"max_positions\": 3, \"max_total_exposure_pct\": 100.0}\n        if regime == \"SIDEWAYS\":\n            return {\"mode\": \"SIDEWAYS_LIMITED\", \"max_positions\": 2, \"max_total_exposure_pct\": 33.3}\n        if regime == \"DOWNTREND\":\n            return {\"mode\": \"DOWNTREND_DEFENSIVE\", \"max_positions\": 1, \"max_total_exposure_pct\": 10.0}\n        if regime == \"N/A\":\n            return {\"mode\": \"N/A\", \"max_positions\": None, \"max_total_exposure_pct\": None}\n        return {\"mode\": \"UNCLASSIFIED_DEFENSIVE\", \"max_positions\": 0, \"max_total_exposure_pct\": 0.0}\n\n    def _e1r_dominant_regime(weights: dict) -> str:\n        if not weights:\n            return \"UNCLASSIFIED\" if e1r_regime_wiring_enabled else \"N/A\""
  },
  {
    "path": "src/engine/backtest.py",
    "function": "run_strategy_variant_comparison",
    "line": 2489,
    "matched_keywords": [
      "compose_e1r_v0_2_variant",
      "build_e1r_sidecar_sleeve",
      "run_stateful_simulation",
      "SIDEWAYS",
      "MA_CONFLICT",
      "gross_exposure",
      "candidate_top_n",
      "entry_top_n"
    ],
    "args": [
      "symbols",
      "prices_map",
      "dates_map",
      "spx_prices",
      "spx_dates",
      "ndx_prices",
      "ndx_dates",
      "sox_prices",
      "sox_dates",
      "vix_prices",
      "vix_dates"
    ],
    "source_head": "def run_strategy_variant_comparison(\n    symbols: list[str],\n    prices_map: dict[str, list[float]],\n    dates_map: dict[str, list[str]],\n    spx_prices: list[float],\n    spx_dates: list[str],\n    ndx_prices: list[float] = None,\n    ndx_dates:  list[str]   = None,\n    sox_prices: list[float] = None,\n    sox_dates:  list[str]   = None,\n    vix_prices: list[float] = None,\n    vix_dates:  list[str]   = None,\n) -> dict:\n    \"\"\"\n    Run four diagnostic portfolio variants using Strict Top3, no fixed TP.\n\n    V0_BASE: current Strict Top3 baseline.\n    V1_RS95: raise entry RS threshold from 90 to 95.\n    V2_RS95_MINHOLD5: add minimum 5 trading-day hold for ordinary REDUCE/EXIT.\n    V3_RS95_MINHOLD5_RELSTOP8: add relative SPX underperformance stop.\n\n    Selection policy:\n    1. Prefer PASS over PARTIAL over FAIL.\n    2. Within the same status, prefer higher total return.\n    3. Break ties with higher Profit Factor, higher Sharpe, then lower max drawdown.\n    \"\"\"\n    logger.info(\"[Backtest Layer D v1.6] Strategy Variant Comparison...\")\n\n    base = {\n        **LAYER_D_ASSUMPTIONS,\n        \"market_gate_enabled\": False,\n        \"market_shock_gate_enabled\": False,\n        \"partial_take_profit_enabled\": False,\n        \"block_add_after_take_profit\": False,\n    }\n    # ── Gate v2 No VIX（冻结市场层基准）─────────────────────────\n    _gate_v2_no_vix = {\n        \"market_gate_enabled\":       True,\n        \"risk_off_below_spx_ma50\":   True,\n        \"market_shock_gate_enabled\": True,\n        \"market_shock_daily_return\": -0.02,\n        \"candidate_top_n\":           None,\n        \"qualified_entry_enabled\":   False,\n        \"fill_only_enabled\":         False,\n    }\n\n    # ── E2 实验配置（Gate 固定 G4，只改退出层）────────────────\n    _gate_g4 = {\n        \"market_gate_enabled\":       True,\n        \"risk_off_below_spx_ma50\":   False,\n        \"market_shock_gate_enabled\": False,\n        \"market_shock_daily_return\": -0.02,\n        \"gate_use_slope\":            True,\n        \"gate_use_leadership\":       True,\n        \"candidate_top_n\":           None,\n        \"qualified_entry_enabled\":   False,\n        \"fill_only_enabled\":         False,\n        \"entry_top_n\":               3,\n        \"entry_rs_min\":              90.0,\n        \"ls60_exit_mode\":            \"exit\",\n    }\n\n    def _load_e1r_regime_daily() -> dict:\n        regime_path = Path(\"data/research/e1_5y/regimes/spx_regime_daily.json\")\n        if not regime_path.exists():\n            logger.warn(f\"  E1-R regime wiring: missing {regime_path}\")\n            return {}\n        try:\n            obj = json.loads(regime_path.read_text())\n        except Exception as exc:\n            logger.warn(f\"  E1-R regime wiring: failed to load {regime_path}: {exc}\")\n            return {}\n        daily = obj.get(\"daily_regime\", obj) if isinstance(obj, dict) else {}\n        return daily if isinstance(daily, dict) else {}\n\n    _e1r_regime_daily = _load_e1r_regime_daily()\n\n    variants = {\n        # E1: Gate G4 + MinHold10（审计对照基准，不可修改）\n        \"E1_AUDITED_G4_MINHOLD10\": {"
  },
  {
    "path": "src/engine/backtest.py",
    "function": "_e1r_mode_for_regime",
    "line": 818,
    "matched_keywords": [
      "SIDEWAYS",
      "DOWNTREND"
    ],
    "args": [
      "regime"
    ],
    "source_head": "def _e1r_mode_for_regime(regime: str) -> str:\n        if regime == \"UPTREND\":\n            return \"UPTREND_EMERGING_CONFIRMED_ENABLED\"\n        if regime == \"SIDEWAYS\":\n            return \"SIDEWAYS_QUALITY_BREAKOUT_ONLY\"\n        if regime == \"DOWNTREND\":\n            return \"DOWNTREND_EXCEPTION_ONLY\"\n        if regime == \"N/A\":\n            return \"N/A\"\n        return \"UNCLASSIFIED_NO_RISK_EXPANSION\""
  },
  {
    "path": "src/engine/backtest.py",
    "function": "_e1r_risk_budget_for_regime",
    "line": 829,
    "matched_keywords": [
      "SIDEWAYS",
      "DOWNTREND",
      "max_positions"
    ],
    "args": [
      "regime"
    ],
    "source_head": "def _e1r_risk_budget_for_regime(regime: str) -> dict:\n        if regime == \"UPTREND\":\n            return {\"mode\": \"UPTREND_RISK_ON\", \"max_positions\": 3, \"max_total_exposure_pct\": 100.0}\n        if regime == \"SIDEWAYS\":\n            return {\"mode\": \"SIDEWAYS_LIMITED\", \"max_positions\": 2, \"max_total_exposure_pct\": 33.3}\n        if regime == \"DOWNTREND\":\n            return {\"mode\": \"DOWNTREND_DEFENSIVE\", \"max_positions\": 1, \"max_total_exposure_pct\": 10.0}\n        if regime == \"N/A\":\n            return {\"mode\": \"N/A\", \"max_positions\": None, \"max_total_exposure_pct\": None}\n        return {\"mode\": \"UNCLASSIFIED_DEFENSIVE\", \"max_positions\": 0, \"max_total_exposure_pct\": 0.0}"
  }
]
```

## Keyword Contexts
```json
[
  {
    "path": "src/engine/e1r_composer.py",
    "exists": true,
    "hit_count": 6,
    "hits": [
      {
        "line": 164,
        "keyword": "gross_exposure",
        "text": "\"sidecar_gross_exposure\": sidecar.get(\"gross_exposure\"),",
        "context": [
          {
            "line": 161,
            "text": "            \"subclass\": sidecar.get(\"subclass\"),"
          },
          {
            "line": 162,
            "text": "            \"sidecar_active\": bool(sidecar.get(\"is_active\")),"
          },
          {
            "line": 163,
            "text": "            \"sidecar_selected_count\": sidecar.get(\"selected_count\"),"
          },
          {
            "line": 164,
            "text": "            \"sidecar_gross_exposure\": sidecar.get(\"gross_exposure\"),"
          },
          {
            "line": 165,
            "text": "            \"sidecar_holdings\": sidecar.get(\"holdings\", []),"
          },
          {
            "line": 166,
            "text": "        })"
          },
          {
            "line": 167,
            "text": ""
          }
        ]
      },
      {
        "line": 208,
        "keyword": "gross_exposure",
        "text": "\"sidecar_gross_exposure\": row.get(\"sidecar_gross_exposure\"),",
        "context": [
          {
            "line": 205,
            "text": "            \"sideways_subclass\": row.get(\"subclass\"),"
          },
          {
            "line": 206,
            "text": "            \"sidecar_active\": row.get(\"sidecar_active\"),"
          },
          {
            "line": 207,
            "text": "            \"sidecar_selected_count\": row.get(\"sidecar_selected_count\"),"
          },
          {
            "line": 208,
            "text": "            \"sidecar_gross_exposure\": row.get(\"sidecar_gross_exposure\"),"
          },
          {
            "line": 209,
            "text": "        })"
          },
          {
            "line": 210,
            "text": ""
          },
          {
            "line": 211,
            "text": "    return records"
          }
        ]
      },
      {
        "line": 283,
        "keyword": "compose_e1r_v0_2_variant",
        "text": "def compose_e1r_v0_2_variant(",
        "context": [
          {
            "line": 280,
            "text": "    }"
          },
          {
            "line": 281,
            "text": ""
          },
          {
            "line": 282,
            "text": ""
          },
          {
            "line": 283,
            "text": "def compose_e1r_v0_2_variant("
          },
          {
            "line": 284,
            "text": "    core_variant_result: dict[str, Any],"
          },
          {
            "line": 285,
            "text": "    sidecar_result: dict[str, Any],"
          },
          {
            "line": 286,
            "text": "    initial_equity: float = 100000.0,"
          }
        ]
      },
      {
        "line": 351,
        "keyword": "SIDEWAYS",
        "text": "\"regime_aware_logic\": \"UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE\",",
        "context": [
          {
            "line": 348,
            "text": ""
          },
          {
            "line": 349,
            "text": "    result.setdefault(\"strategy_controls\", {})"
          },
          {
            "line": 350,
            "text": "    result[\"strategy_controls\"].update({"
          },
          {
            "line": 351,
            "text": "        \"regime_aware_logic\": \"UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE\","
          },
          {
            "line": 352,
            "text": "        \"e1r_v0_2_formal_sidecar_sleeve\": True,"
          },
          {
            "line": 353,
            "text": "        \"e1r_v0_2_core_variant\": \"E1R_REGIME_AWARE_V0_1\","
          },
          {
            "line": 354,
            "text": "        \"e1r_v0_2_sidecar_allowed_subclasses\": sidecar_result.get(\"config\", {}).get(\"allowed_subclasses\"),"
          }
        ]
      },
      {
        "line": 351,
        "keyword": "MA_CONFLICT",
        "text": "\"regime_aware_logic\": \"UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE\",",
        "context": [
          {
            "line": 348,
            "text": ""
          },
          {
            "line": 349,
            "text": "    result.setdefault(\"strategy_controls\", {})"
          },
          {
            "line": 350,
            "text": "    result[\"strategy_controls\"].update({"
          },
          {
            "line": 351,
            "text": "        \"regime_aware_logic\": \"UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE\","
          },
          {
            "line": 352,
            "text": "        \"e1r_v0_2_formal_sidecar_sleeve\": True,"
          },
          {
            "line": 353,
            "text": "        \"e1r_v0_2_core_variant\": \"E1R_REGIME_AWARE_V0_1\","
          },
          {
            "line": 354,
            "text": "        \"e1r_v0_2_sidecar_allowed_subclasses\": sidecar_result.get(\"config\", {}).get(\"allowed_subclasses\"),"
          }
        ]
      },
      {
        "line": 356,
        "keyword": "gross_exposure",
        "text": "\"e1r_v0_2_sidecar_gross_exposure\": sidecar_result.get(\"config\", {}).get(\"gross_exposure\"),",
        "context": [
          {
            "line": 353,
            "text": "        \"e1r_v0_2_core_variant\": \"E1R_REGIME_AWARE_V0_1\","
          },
          {
            "line": 354,
            "text": "        \"e1r_v0_2_sidecar_allowed_subclasses\": sidecar_result.get(\"config\", {}).get(\"allowed_subclasses\"),"
          },
          {
            "line": 355,
            "text": "        \"e1r_v0_2_sidecar_top_n\": sidecar_result.get(\"config\", {}).get(\"top_n\"),"
          },
          {
            "line": 356,
            "text": "        \"e1r_v0_2_sidecar_gross_exposure\": sidecar_result.get(\"config\", {}).get(\"gross_exposure\"),"
          },
          {
            "line": 357,
            "text": "        \"e1r_v0_2_excluded_symbols\": sidecar_result.get(\"config\", {}).get(\"excluded_symbols\"),"
          },
          {
            "line": 358,
            "text": "    })"
          },
          {
            "line": 359,
            "text": ""
          }
        ]
      }
    ]
  },
  {
    "path": "src/engine/e1r_sidecar_sleeve.py",
    "exists": true,
    "hit_count": 19,
    "hits": [
      {
        "line": 10,
        "keyword": "SIDEWAYS",
        "text": "- Active only in SIDEWAYS:MA_CONFLICT.",
        "context": [
          {
            "line": 7,
            "text": ""
          },
          {
            "line": 8,
            "text": "This module implements the same rule semantics that passed research validation:"
          },
          {
            "line": 9,
            "text": ""
          },
          {
            "line": 10,
            "text": "- Active only in SIDEWAYS:MA_CONFLICT."
          },
          {
            "line": 11,
            "text": "- Top-N basket selection."
          },
          {
            "line": 12,
            "text": "- Gross exposure sleeve, default 25%."
          },
          {
            "line": 13,
            "text": "- Daily close-to-close rebalance."
          }
        ]
      },
      {
        "line": 10,
        "keyword": "MA_CONFLICT",
        "text": "- Active only in SIDEWAYS:MA_CONFLICT.",
        "context": [
          {
            "line": 7,
            "text": ""
          },
          {
            "line": 8,
            "text": "This module implements the same rule semantics that passed research validation:"
          },
          {
            "line": 9,
            "text": ""
          },
          {
            "line": 10,
            "text": "- Active only in SIDEWAYS:MA_CONFLICT."
          },
          {
            "line": 11,
            "text": "- Top-N basket selection."
          },
          {
            "line": 12,
            "text": "- Gross exposure sleeve, default 25%."
          },
          {
            "line": 13,
            "text": "- Daily close-to-close rebalance."
          }
        ]
      },
      {
        "line": 15,
        "keyword": "DOWNTREND",
        "text": "- DOWNTREND / RECOVERY / DETERIORATION have zero sleeve exposure.",
        "context": [
          {
            "line": 12,
            "text": "- Gross exposure sleeve, default 25%."
          },
          {
            "line": 13,
            "text": "- Daily close-to-close rebalance."
          },
          {
            "line": 14,
            "text": "- VIXY excluded by default."
          },
          {
            "line": 15,
            "text": "- DOWNTREND / RECOVERY / DETERIORATION have zero sleeve exposure."
          },
          {
            "line": 16,
            "text": ""
          },
          {
            "line": 17,
            "text": "Important"
          },
          {
            "line": 18,
            "text": "---------"
          }
        ]
      },
      {
        "line": 19,
        "keyword": "run_stateful_simulation",
        "text": "This is intentionally separate from run_stateful_simulation().",
        "context": [
          {
            "line": 16,
            "text": ""
          },
          {
            "line": 17,
            "text": "Important"
          },
          {
            "line": 18,
            "text": "---------"
          },
          {
            "line": 19,
            "text": "This is intentionally separate from run_stateful_simulation()."
          },
          {
            "line": 20,
            "text": ""
          },
          {
            "line": 21,
            "text": "The existing stateful Top3 engine remains responsible for:"
          },
          {
            "line": 22,
            "text": "- E1_AUDITED_G4_MINHOLD10"
          }
        ]
      },
      {
        "line": 44,
        "keyword": "MA_CONFLICT",
        "text": "allowed_subclasses: tuple[str, ...] = (\"MA_CONFLICT\",)",
        "context": [
          {
            "line": 41,
            "text": "class E1RSidecarConfig:"
          },
          {
            "line": 42,
            "text": "    start_date: str"
          },
          {
            "line": 43,
            "text": "    end_date: str"
          },
          {
            "line": 44,
            "text": "    allowed_subclasses: tuple[str, ...] = (\"MA_CONFLICT\",)"
          },
          {
            "line": 45,
            "text": "    top_n: int = 10"
          },
          {
            "line": 46,
            "text": "    gross_exposure: float = 0.25"
          },
          {
            "line": 47,
            "text": "    min_history_days: int = 200"
          }
        ]
      },
      {
        "line": 46,
        "keyword": "gross_exposure",
        "text": "gross_exposure: float = 0.25",
        "context": [
          {
            "line": 43,
            "text": "    end_date: str"
          },
          {
            "line": 44,
            "text": "    allowed_subclasses: tuple[str, ...] = (\"MA_CONFLICT\",)"
          },
          {
            "line": 45,
            "text": "    top_n: int = 10"
          },
          {
            "line": 46,
            "text": "    gross_exposure: float = 0.25"
          },
          {
            "line": 47,
            "text": "    min_history_days: int = 200"
          },
          {
            "line": 48,
            "text": "    min_price: float = 5.0"
          },
          {
            "line": 49,
            "text": "    initial_equity: float = 100000.0"
          }
        ]
      },
      {
        "line": 367,
        "keyword": "SIDEWAYS",
        "text": "if regime_info.get(\"regime\") != \"SIDEWAYS\":",
        "context": [
          {
            "line": 364,
            "text": ""
          },
          {
            "line": 365,
            "text": "    for date, next_date in intervals:"
          },
          {
            "line": 366,
            "text": "        regime_info = regimes.get(date, {})"
          },
          {
            "line": 367,
            "text": "        if regime_info.get(\"regime\") != \"SIDEWAYS\":"
          },
          {
            "line": 368,
            "text": "            continue"
          },
          {
            "line": 369,
            "text": ""
          },
          {
            "line": 370,
            "text": "        candidates: list[dict[str, Any]] = []"
          }
        ]
      },
      {
        "line": 392,
        "keyword": "SIDEWAYS",
        "text": "\"regime\": \"SIDEWAYS\",",
        "context": [
          {
            "line": 389,
            "text": "        rankings[date] = {"
          },
          {
            "line": 390,
            "text": "            \"date\": date,"
          },
          {
            "line": 391,
            "text": "            \"next_date\": next_date,"
          },
          {
            "line": 392,
            "text": "            \"regime\": \"SIDEWAYS\","
          },
          {
            "line": 393,
            "text": "            \"subclass\": regime_info.get(\"subclass\") or \"NO_SUBCLASS\","
          },
          {
            "line": 394,
            "text": "            \"candidate_count\": len(candidates),"
          },
          {
            "line": 395,
            "text": "            \"candidates\": candidates,"
          }
        ]
      },
      {
        "line": 410,
        "keyword": "gross_exposure",
        "text": "gross_exposure = float(config.gross_exposure)",
        "context": [
          {
            "line": 407,
            "text": ") -> list[dict[str, Any]]:"
          },
          {
            "line": 408,
            "text": "    allowed_subclasses = set(config.allowed_subclasses)"
          },
          {
            "line": 409,
            "text": "    top_n = int(config.top_n)"
          },
          {
            "line": 410,
            "text": "    gross_exposure = float(config.gross_exposure)"
          },
          {
            "line": 411,
            "text": ""
          },
          {
            "line": 412,
            "text": "    records: list[dict[str, Any]] = []"
          },
          {
            "line": 413,
            "text": ""
          }
        ]
      },
      {
        "line": 425,
        "keyword": "SIDEWAYS",
        "text": "regime == \"SIDEWAYS\"",
        "context": [
          {
            "line": 422,
            "text": "        candidates = ranked.get(\"candidates\", [])"
          },
          {
            "line": 423,
            "text": ""
          },
          {
            "line": 424,
            "text": "        is_active = ("
          },
          {
            "line": 425,
            "text": "            regime == \"SIDEWAYS\""
          },
          {
            "line": 426,
            "text": "            and subclass in allowed_subclasses"
          },
          {
            "line": 427,
            "text": "            and top_n > 0"
          },
          {
            "line": 428,
            "text": "            and gross_exposure > 0"
          }
        ]
      },
      {
        "line": 428,
        "keyword": "gross_exposure",
        "text": "and gross_exposure > 0",
        "context": [
          {
            "line": 425,
            "text": "            regime == \"SIDEWAYS\""
          },
          {
            "line": 426,
            "text": "            and subclass in allowed_subclasses"
          },
          {
            "line": 427,
            "text": "            and top_n > 0"
          },
          {
            "line": 428,
            "text": "            and gross_exposure > 0"
          },
          {
            "line": 429,
            "text": "            and bool(candidates)"
          },
          {
            "line": 430,
            "text": "        )"
          },
          {
            "line": 431,
            "text": ""
          }
        ]
      },
      {
        "line": 437,
        "keyword": "gross_exposure",
        "text": "weight = gross_exposure / len(selected)",
        "context": [
          {
            "line": 434,
            "text": ""
          },
          {
            "line": 435,
            "text": "        if is_active:"
          },
          {
            "line": 436,
            "text": "            selected = candidates[:top_n]"
          },
          {
            "line": 437,
            "text": "            weight = gross_exposure / len(selected)"
          },
          {
            "line": 438,
            "text": ""
          },
          {
            "line": 439,
            "text": "            for candidate in selected:"
          },
          {
            "line": 440,
            "text": "                raw_return = candidate[\"one_day_return\"]"
          }
        ]
      },
      {
        "line": 462,
        "keyword": "gross_exposure",
        "text": "\"gross_exposure\": gross_exposure if is_active else 0.0,",
        "context": [
          {
            "line": 459,
            "text": "            \"is_active\": is_active,"
          },
          {
            "line": 460,
            "text": "            \"candidate_count\": len(candidates),"
          },
          {
            "line": 461,
            "text": "            \"selected_count\": len(holdings),"
          },
          {
            "line": 462,
            "text": "            \"gross_exposure\": gross_exposure if is_active else 0.0,"
          },
          {
            "line": 463,
            "text": "            \"portfolio_return\": portfolio_return,"
          },
          {
            "line": 464,
            "text": "            \"portfolio_return_pct\": pct_display(portfolio_return),"
          },
          {
            "line": 465,
            "text": "            \"spx_return\": spx_return,"
          }
        ]
      },
      {
        "line": 498,
        "keyword": "SIDEWAYS",
        "text": "\"name\": \"E1R_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE\",",
        "context": [
          {
            "line": 495,
            "text": "    losses = [r for r in active_records if r[\"portfolio_return\"] < 0]"
          },
          {
            "line": 496,
            "text": ""
          },
          {
            "line": 497,
            "text": "    return {"
          },
          {
            "line": 498,
            "text": "        \"name\": \"E1R_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE\","
          },
          {
            "line": 499,
            "text": "        \"allowed_subclasses\": list(config.allowed_subclasses),"
          },
          {
            "line": 500,
            "text": "        \"top_n\": config.top_n,"
          },
          {
            "line": 501,
            "text": "        \"gross_exposure\": config.gross_exposure,"
          }
        ]
      },
      {
        "line": 498,
        "keyword": "MA_CONFLICT",
        "text": "\"name\": \"E1R_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE\",",
        "context": [
          {
            "line": 495,
            "text": "    losses = [r for r in active_records if r[\"portfolio_return\"] < 0]"
          },
          {
            "line": 496,
            "text": ""
          },
          {
            "line": 497,
            "text": "    return {"
          },
          {
            "line": 498,
            "text": "        \"name\": \"E1R_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE\","
          },
          {
            "line": 499,
            "text": "        \"allowed_subclasses\": list(config.allowed_subclasses),"
          },
          {
            "line": 500,
            "text": "        \"top_n\": config.top_n,"
          },
          {
            "line": 501,
            "text": "        \"gross_exposure\": config.gross_exposure,"
          }
        ]
      },
      {
        "line": 501,
        "keyword": "gross_exposure",
        "text": "\"gross_exposure\": config.gross_exposure,",
        "context": [
          {
            "line": 498,
            "text": "        \"name\": \"E1R_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE\","
          },
          {
            "line": 499,
            "text": "        \"allowed_subclasses\": list(config.allowed_subclasses),"
          },
          {
            "line": 500,
            "text": "        \"top_n\": config.top_n,"
          },
          {
            "line": 501,
            "text": "        \"gross_exposure\": config.gross_exposure,"
          },
          {
            "line": 502,
            "text": "        \"excluded_symbols\": list(config.excluded_symbols),"
          },
          {
            "line": 503,
            "text": ""
          },
          {
            "line": 504,
            "text": "        \"total_days\": len(records),"
          }
        ]
      },
      {
        "line": 538,
        "keyword": "build_e1r_sidecar_sleeve",
        "text": "def build_e1r_sidecar_sleeve(",
        "context": [
          {
            "line": 535,
            "text": "    }"
          },
          {
            "line": 536,
            "text": ""
          },
          {
            "line": 537,
            "text": ""
          },
          {
            "line": 538,
            "text": "def build_e1r_sidecar_sleeve("
          },
          {
            "line": 539,
            "text": "    stock_dir: Path,"
          },
          {
            "line": 540,
            "text": "    spx_path: Path,"
          },
          {
            "line": 541,
            "text": "    regime_path: Path,"
          }
        ]
      },
      {
        "line": 560,
        "keyword": "SIDEWAYS",
        "text": "if regime == \"SIDEWAYS\":",
        "context": [
          {
            "line": 557,
            "text": "        regime = record[\"regime\"]"
          },
          {
            "line": 558,
            "text": "        subclass = record[\"subclass\"]"
          },
          {
            "line": 559,
            "text": "        regime_counts[regime] = regime_counts.get(regime, 0) + 1"
          },
          {
            "line": 560,
            "text": "        if regime == \"SIDEWAYS\":"
          },
          {
            "line": 561,
            "text": "            subclass_counts[subclass] = subclass_counts.get(subclass, 0) + 1"
          },
          {
            "line": 562,
            "text": ""
          },
          {
            "line": 563,
            "text": "    return {"
          }
        ]
      },
      {
        "line": 571,
        "keyword": "gross_exposure",
        "text": "\"gross_exposure\": config.gross_exposure,",
        "context": [
          {
            "line": 568,
            "text": "            \"end_date\": config.end_date,"
          },
          {
            "line": 569,
            "text": "            \"allowed_subclasses\": list(config.allowed_subclasses),"
          },
          {
            "line": 570,
            "text": "            \"top_n\": config.top_n,"
          },
          {
            "line": 571,
            "text": "            \"gross_exposure\": config.gross_exposure,"
          },
          {
            "line": 572,
            "text": "            \"min_history_days\": config.min_history_days,"
          },
          {
            "line": 573,
            "text": "            \"min_price\": config.min_price,"
          },
          {
            "line": 574,
            "text": "            \"initial_equity\": config.initial_equity,"
          }
        ]
      }
    ]
  },
  {
    "path": "src/engine/backtest.py",
    "exists": true,
    "hit_count": 69,
    "hits": [
      {
        "line": 35,
        "keyword": "max_positions",
        "text": "\"max_positions\":      3,",
        "context": [
          {
            "line": 32,
            "text": "# ══════════════════════════════════════════════════════════════════"
          },
          {
            "line": 33,
            "text": "LAYER_D_ASSUMPTIONS = {"
          },
          {
            "line": 34,
            "text": "    \"initial_capital\":   100_000,"
          },
          {
            "line": 35,
            "text": "    \"max_positions\":      3,"
          },
          {
            "line": 36,
            "text": "    \"buy_size\":          1.0,    # Top3: 1/3 portfolio full position"
          },
          {
            "line": 37,
            "text": "    \"add_size\":          0.5,    # Top3: +1/6 portfolio, used only after REDUCE if allowed"
          },
          {
            "line": 38,
            "text": "    \"max_single_size\":   1.0,    # Top3 strategy: 1/3 max per position"
          }
        ]
      },
      {
        "line": 55,
        "keyword": "entry_top_n",
        "text": "\"entry_top_n\":       3,",
        "context": [
          {
            "line": 52,
            "text": "    \"leverage\":          False,"
          },
          {
            "line": 53,
            "text": "    \"short_selling\":     False,"
          },
          {
            "line": 54,
            "text": "    \"strategy_variant\":  \"top3_entry_rs_minhold_relstop\","
          },
          {
            "line": 55,
            "text": "    \"entry_top_n\":       3,"
          },
          {
            "line": 56,
            "text": "    \"rank_based_exit\":   False,"
          },
          {
            "line": 57,
            "text": "    # Market Gate is disabled in this v1.6 diagnostic matrix so we can isolate"
          },
          {
            "line": 58,
            "text": "    # the impact of RS threshold, minimum holding period, and relative SPX stop."
          }
        ]
      },
      {
        "line": 82,
        "keyword": "candidate_top_n",
        "text": "# candidate_top_n：Qualified Pool 内最多取 N 个候选（None = 用旧 entry_top_n 逻辑）",
        "context": [
          {
            "line": 79,
            "text": "    \"ls60_exit_mode\":    \"reduce\",   # \"exit\"=旧规则 \"reduce\"=新规则（默认）"
          },
          {
            "line": 80,
            "text": ""
          },
          {
            "line": 81,
            "text": "    # Qualified Candidate Pool（v1.7+）"
          },
          {
            "line": 82,
            "text": "    # candidate_top_n：Qualified Pool 内最多取 N 个候选（None = 用旧 entry_top_n 逻辑）"
          },
          {
            "line": 83,
            "text": "    # max_positions：组合最大持仓数"
          },
          {
            "line": 84,
            "text": "    # qualified_entry_enabled：是否启用资格过滤"
          },
          {
            "line": 85,
            "text": "    # qualified_states：允许的 trend_state"
          }
        ]
      },
      {
        "line": 82,
        "keyword": "entry_top_n",
        "text": "# candidate_top_n：Qualified Pool 内最多取 N 个候选（None = 用旧 entry_top_n 逻辑）",
        "context": [
          {
            "line": 79,
            "text": "    \"ls60_exit_mode\":    \"reduce\",   # \"exit\"=旧规则 \"reduce\"=新规则（默认）"
          },
          {
            "line": 80,
            "text": ""
          },
          {
            "line": 81,
            "text": "    # Qualified Candidate Pool（v1.7+）"
          },
          {
            "line": 82,
            "text": "    # candidate_top_n：Qualified Pool 内最多取 N 个候选（None = 用旧 entry_top_n 逻辑）"
          },
          {
            "line": 83,
            "text": "    # max_positions：组合最大持仓数"
          },
          {
            "line": 84,
            "text": "    # qualified_entry_enabled：是否启用资格过滤"
          },
          {
            "line": 85,
            "text": "    # qualified_states：允许的 trend_state"
          }
        ]
      },
      {
        "line": 83,
        "keyword": "max_positions",
        "text": "# max_positions：组合最大持仓数",
        "context": [
          {
            "line": 80,
            "text": ""
          },
          {
            "line": 81,
            "text": "    # Qualified Candidate Pool（v1.7+）"
          },
          {
            "line": 82,
            "text": "    # candidate_top_n：Qualified Pool 内最多取 N 个候选（None = 用旧 entry_top_n 逻辑）"
          },
          {
            "line": 83,
            "text": "    # max_positions：组合最大持仓数"
          },
          {
            "line": 84,
            "text": "    # qualified_entry_enabled：是否启用资格过滤"
          },
          {
            "line": 85,
            "text": "    # qualified_states：允许的 trend_state"
          },
          {
            "line": 86,
            "text": "    \"candidate_top_n\":          None,    # None = 沿用旧 entry_top_n=3 逻辑"
          }
        ]
      },
      {
        "line": 86,
        "keyword": "candidate_top_n",
        "text": "\"candidate_top_n\":          None,    # None = 沿用旧 entry_top_n=3 逻辑",
        "context": [
          {
            "line": 83,
            "text": "    # max_positions：组合最大持仓数"
          },
          {
            "line": 84,
            "text": "    # qualified_entry_enabled：是否启用资格过滤"
          },
          {
            "line": 85,
            "text": "    # qualified_states：允许的 trend_state"
          },
          {
            "line": 86,
            "text": "    \"candidate_top_n\":          None,    # None = 沿用旧 entry_top_n=3 逻辑"
          },
          {
            "line": 87,
            "text": "    \"qualified_entry_enabled\":  False,"
          },
          {
            "line": 88,
            "text": "    \"qualified_rs_min\":         90.0,"
          },
          {
            "line": 89,
            "text": "    \"qualified_momentum_min\":   85.0,"
          }
        ]
      },
      {
        "line": 86,
        "keyword": "entry_top_n",
        "text": "\"candidate_top_n\":          None,    # None = 沿用旧 entry_top_n=3 逻辑",
        "context": [
          {
            "line": 83,
            "text": "    # max_positions：组合最大持仓数"
          },
          {
            "line": 84,
            "text": "    # qualified_entry_enabled：是否启用资格过滤"
          },
          {
            "line": 85,
            "text": "    # qualified_states：允许的 trend_state"
          },
          {
            "line": 86,
            "text": "    \"candidate_top_n\":          None,    # None = 沿用旧 entry_top_n=3 逻辑"
          },
          {
            "line": 87,
            "text": "    \"qualified_entry_enabled\":  False,"
          },
          {
            "line": 88,
            "text": "    \"qualified_rs_min\":         90.0,"
          },
          {
            "line": 89,
            "text": "    \"qualified_momentum_min\":   85.0,"
          }
        ]
      },
      {
        "line": 763,
        "keyword": "run_stateful_simulation",
        "text": "def run_stateful_simulation(",
        "context": [
          {
            "line": 760,
            "text": "# Layer D: Stateful Strategy Simulation"
          },
          {
            "line": 761,
            "text": "# ══════════════════════════════════════════════════════════════════"
          },
          {
            "line": 762,
            "text": ""
          },
          {
            "line": 763,
            "text": "def run_stateful_simulation("
          },
          {
            "line": 764,
            "text": "    symbols:        list[str],"
          },
          {
            "line": 765,
            "text": "    prices_map:     dict[str, list[float]],"
          },
          {
            "line": 766,
            "text": "    dates_map:      dict[str, list[str]],"
          }
        ]
      },
      {
        "line": 796,
        "keyword": "max_positions",
        "text": "max_pos  = a[\"max_positions\"]",
        "context": [
          {
            "line": 793,
            "text": ""
          },
          {
            "line": 794,
            "text": "    # ── 冻结参数 ─────────────────────────────────────────"
          },
          {
            "line": 795,
            "text": "    a        = assumptions or LAYER_D_ASSUMPTIONS"
          },
          {
            "line": 796,
            "text": "    max_pos  = a[\"max_positions\"]"
          },
          {
            "line": 797,
            "text": "    buy_pct  = a[\"buy_size\"]  / max_pos       # Top3: 1/3 per full slot"
          },
          {
            "line": 798,
            "text": "    add_pct  = a[\"add_size\"]  / max_pos       # Top3: +1/6, only useful after REDUCE"
          },
          {
            "line": 799,
            "text": "    max_pct  = a[\"max_single_size\"] / max_pos # Top3: max 1/3 per position"
          }
        ]
      },
      {
        "line": 821,
        "keyword": "SIDEWAYS",
        "text": "if regime == \"SIDEWAYS\":",
        "context": [
          {
            "line": 818,
            "text": "    def _e1r_mode_for_regime(regime: str) -> str:"
          },
          {
            "line": 819,
            "text": "        if regime == \"UPTREND\":"
          },
          {
            "line": 820,
            "text": "            return \"UPTREND_EMERGING_CONFIRMED_ENABLED\""
          },
          {
            "line": 821,
            "text": "        if regime == \"SIDEWAYS\":"
          },
          {
            "line": 822,
            "text": "            return \"SIDEWAYS_QUALITY_BREAKOUT_ONLY\""
          },
          {
            "line": 823,
            "text": "        if regime == \"DOWNTREND\":"
          },
          {
            "line": 824,
            "text": "            return \"DOWNTREND_EXCEPTION_ONLY\""
          }
        ]
      },
      {
        "line": 822,
        "keyword": "SIDEWAYS",
        "text": "return \"SIDEWAYS_QUALITY_BREAKOUT_ONLY\"",
        "context": [
          {
            "line": 819,
            "text": "        if regime == \"UPTREND\":"
          },
          {
            "line": 820,
            "text": "            return \"UPTREND_EMERGING_CONFIRMED_ENABLED\""
          },
          {
            "line": 821,
            "text": "        if regime == \"SIDEWAYS\":"
          },
          {
            "line": 822,
            "text": "            return \"SIDEWAYS_QUALITY_BREAKOUT_ONLY\""
          },
          {
            "line": 823,
            "text": "        if regime == \"DOWNTREND\":"
          },
          {
            "line": 824,
            "text": "            return \"DOWNTREND_EXCEPTION_ONLY\""
          },
          {
            "line": 825,
            "text": "        if regime == \"N/A\":"
          }
        ]
      },
      {
        "line": 823,
        "keyword": "DOWNTREND",
        "text": "if regime == \"DOWNTREND\":",
        "context": [
          {
            "line": 820,
            "text": "            return \"UPTREND_EMERGING_CONFIRMED_ENABLED\""
          },
          {
            "line": 821,
            "text": "        if regime == \"SIDEWAYS\":"
          },
          {
            "line": 822,
            "text": "            return \"SIDEWAYS_QUALITY_BREAKOUT_ONLY\""
          },
          {
            "line": 823,
            "text": "        if regime == \"DOWNTREND\":"
          },
          {
            "line": 824,
            "text": "            return \"DOWNTREND_EXCEPTION_ONLY\""
          },
          {
            "line": 825,
            "text": "        if regime == \"N/A\":"
          },
          {
            "line": 826,
            "text": "            return \"N/A\""
          }
        ]
      },
      {
        "line": 824,
        "keyword": "DOWNTREND",
        "text": "return \"DOWNTREND_EXCEPTION_ONLY\"",
        "context": [
          {
            "line": 821,
            "text": "        if regime == \"SIDEWAYS\":"
          },
          {
            "line": 822,
            "text": "            return \"SIDEWAYS_QUALITY_BREAKOUT_ONLY\""
          },
          {
            "line": 823,
            "text": "        if regime == \"DOWNTREND\":"
          },
          {
            "line": 824,
            "text": "            return \"DOWNTREND_EXCEPTION_ONLY\""
          },
          {
            "line": 825,
            "text": "        if regime == \"N/A\":"
          },
          {
            "line": 826,
            "text": "            return \"N/A\""
          },
          {
            "line": 827,
            "text": "        return \"UNCLASSIFIED_NO_RISK_EXPANSION\""
          }
        ]
      },
      {
        "line": 831,
        "keyword": "max_positions",
        "text": "return {\"mode\": \"UPTREND_RISK_ON\", \"max_positions\": 3, \"max_total_exposure_pct\": 100.0}",
        "context": [
          {
            "line": 828,
            "text": ""
          },
          {
            "line": 829,
            "text": "    def _e1r_risk_budget_for_regime(regime: str) -> dict:"
          },
          {
            "line": 830,
            "text": "        if regime == \"UPTREND\":"
          },
          {
            "line": 831,
            "text": "            return {\"mode\": \"UPTREND_RISK_ON\", \"max_positions\": 3, \"max_total_exposure_pct\": 100.0}"
          },
          {
            "line": 832,
            "text": "        if regime == \"SIDEWAYS\":"
          },
          {
            "line": 833,
            "text": "            return {\"mode\": \"SIDEWAYS_LIMITED\", \"max_positions\": 2, \"max_total_exposure_pct\": 33.3}"
          },
          {
            "line": 834,
            "text": "        if regime == \"DOWNTREND\":"
          }
        ]
      },
      {
        "line": 832,
        "keyword": "SIDEWAYS",
        "text": "if regime == \"SIDEWAYS\":",
        "context": [
          {
            "line": 829,
            "text": "    def _e1r_risk_budget_for_regime(regime: str) -> dict:"
          },
          {
            "line": 830,
            "text": "        if regime == \"UPTREND\":"
          },
          {
            "line": 831,
            "text": "            return {\"mode\": \"UPTREND_RISK_ON\", \"max_positions\": 3, \"max_total_exposure_pct\": 100.0}"
          },
          {
            "line": 832,
            "text": "        if regime == \"SIDEWAYS\":"
          },
          {
            "line": 833,
            "text": "            return {\"mode\": \"SIDEWAYS_LIMITED\", \"max_positions\": 2, \"max_total_exposure_pct\": 33.3}"
          },
          {
            "line": 834,
            "text": "        if regime == \"DOWNTREND\":"
          },
          {
            "line": 835,
            "text": "            return {\"mode\": \"DOWNTREND_DEFENSIVE\", \"max_positions\": 1, \"max_total_exposure_pct\": 10.0}"
          }
        ]
      },
      {
        "line": 833,
        "keyword": "SIDEWAYS",
        "text": "return {\"mode\": \"SIDEWAYS_LIMITED\", \"max_positions\": 2, \"max_total_exposure_pct\": 33.3}",
        "context": [
          {
            "line": 830,
            "text": "        if regime == \"UPTREND\":"
          },
          {
            "line": 831,
            "text": "            return {\"mode\": \"UPTREND_RISK_ON\", \"max_positions\": 3, \"max_total_exposure_pct\": 100.0}"
          },
          {
            "line": 832,
            "text": "        if regime == \"SIDEWAYS\":"
          },
          {
            "line": 833,
            "text": "            return {\"mode\": \"SIDEWAYS_LIMITED\", \"max_positions\": 2, \"max_total_exposure_pct\": 33.3}"
          },
          {
            "line": 834,
            "text": "        if regime == \"DOWNTREND\":"
          },
          {
            "line": 835,
            "text": "            return {\"mode\": \"DOWNTREND_DEFENSIVE\", \"max_positions\": 1, \"max_total_exposure_pct\": 10.0}"
          },
          {
            "line": 836,
            "text": "        if regime == \"N/A\":"
          }
        ]
      },
      {
        "line": 833,
        "keyword": "max_positions",
        "text": "return {\"mode\": \"SIDEWAYS_LIMITED\", \"max_positions\": 2, \"max_total_exposure_pct\": 33.3}",
        "context": [
          {
            "line": 830,
            "text": "        if regime == \"UPTREND\":"
          },
          {
            "line": 831,
            "text": "            return {\"mode\": \"UPTREND_RISK_ON\", \"max_positions\": 3, \"max_total_exposure_pct\": 100.0}"
          },
          {
            "line": 832,
            "text": "        if regime == \"SIDEWAYS\":"
          },
          {
            "line": 833,
            "text": "            return {\"mode\": \"SIDEWAYS_LIMITED\", \"max_positions\": 2, \"max_total_exposure_pct\": 33.3}"
          },
          {
            "line": 834,
            "text": "        if regime == \"DOWNTREND\":"
          },
          {
            "line": 835,
            "text": "            return {\"mode\": \"DOWNTREND_DEFENSIVE\", \"max_positions\": 1, \"max_total_exposure_pct\": 10.0}"
          },
          {
            "line": 836,
            "text": "        if regime == \"N/A\":"
          }
        ]
      },
      {
        "line": 834,
        "keyword": "DOWNTREND",
        "text": "if regime == \"DOWNTREND\":",
        "context": [
          {
            "line": 831,
            "text": "            return {\"mode\": \"UPTREND_RISK_ON\", \"max_positions\": 3, \"max_total_exposure_pct\": 100.0}"
          },
          {
            "line": 832,
            "text": "        if regime == \"SIDEWAYS\":"
          },
          {
            "line": 833,
            "text": "            return {\"mode\": \"SIDEWAYS_LIMITED\", \"max_positions\": 2, \"max_total_exposure_pct\": 33.3}"
          },
          {
            "line": 834,
            "text": "        if regime == \"DOWNTREND\":"
          },
          {
            "line": 835,
            "text": "            return {\"mode\": \"DOWNTREND_DEFENSIVE\", \"max_positions\": 1, \"max_total_exposure_pct\": 10.0}"
          },
          {
            "line": 836,
            "text": "        if regime == \"N/A\":"
          },
          {
            "line": 837,
            "text": "            return {\"mode\": \"N/A\", \"max_positions\": None, \"max_total_exposure_pct\": None}"
          }
        ]
      },
      {
        "line": 835,
        "keyword": "DOWNTREND",
        "text": "return {\"mode\": \"DOWNTREND_DEFENSIVE\", \"max_positions\": 1, \"max_total_exposure_pct\": 10.0}",
        "context": [
          {
            "line": 832,
            "text": "        if regime == \"SIDEWAYS\":"
          },
          {
            "line": 833,
            "text": "            return {\"mode\": \"SIDEWAYS_LIMITED\", \"max_positions\": 2, \"max_total_exposure_pct\": 33.3}"
          },
          {
            "line": 834,
            "text": "        if regime == \"DOWNTREND\":"
          },
          {
            "line": 835,
            "text": "            return {\"mode\": \"DOWNTREND_DEFENSIVE\", \"max_positions\": 1, \"max_total_exposure_pct\": 10.0}"
          },
          {
            "line": 836,
            "text": "        if regime == \"N/A\":"
          },
          {
            "line": 837,
            "text": "            return {\"mode\": \"N/A\", \"max_positions\": None, \"max_total_exposure_pct\": None}"
          },
          {
            "line": 838,
            "text": "        return {\"mode\": \"UNCLASSIFIED_DEFENSIVE\", \"max_positions\": 0, \"max_total_exposure_pct\": 0.0}"
          }
        ]
      },
      {
        "line": 835,
        "keyword": "max_positions",
        "text": "return {\"mode\": \"DOWNTREND_DEFENSIVE\", \"max_positions\": 1, \"max_total_exposure_pct\": 10.0}",
        "context": [
          {
            "line": 832,
            "text": "        if regime == \"SIDEWAYS\":"
          },
          {
            "line": 833,
            "text": "            return {\"mode\": \"SIDEWAYS_LIMITED\", \"max_positions\": 2, \"max_total_exposure_pct\": 33.3}"
          },
          {
            "line": 834,
            "text": "        if regime == \"DOWNTREND\":"
          },
          {
            "line": 835,
            "text": "            return {\"mode\": \"DOWNTREND_DEFENSIVE\", \"max_positions\": 1, \"max_total_exposure_pct\": 10.0}"
          },
          {
            "line": 836,
            "text": "        if regime == \"N/A\":"
          },
          {
            "line": 837,
            "text": "            return {\"mode\": \"N/A\", \"max_positions\": None, \"max_total_exposure_pct\": None}"
          },
          {
            "line": 838,
            "text": "        return {\"mode\": \"UNCLASSIFIED_DEFENSIVE\", \"max_positions\": 0, \"max_total_exposure_pct\": 0.0}"
          }
        ]
      },
      {
        "line": 837,
        "keyword": "max_positions",
        "text": "return {\"mode\": \"N/A\", \"max_positions\": None, \"max_total_exposure_pct\": None}",
        "context": [
          {
            "line": 834,
            "text": "        if regime == \"DOWNTREND\":"
          },
          {
            "line": 835,
            "text": "            return {\"mode\": \"DOWNTREND_DEFENSIVE\", \"max_positions\": 1, \"max_total_exposure_pct\": 10.0}"
          },
          {
            "line": 836,
            "text": "        if regime == \"N/A\":"
          },
          {
            "line": 837,
            "text": "            return {\"mode\": \"N/A\", \"max_positions\": None, \"max_total_exposure_pct\": None}"
          },
          {
            "line": 838,
            "text": "        return {\"mode\": \"UNCLASSIFIED_DEFENSIVE\", \"max_positions\": 0, \"max_total_exposure_pct\": 0.0}"
          },
          {
            "line": 839,
            "text": ""
          },
          {
            "line": 840,
            "text": "    def _e1r_dominant_regime(weights: dict) -> str:"
          }
        ]
      },
      {
        "line": 838,
        "keyword": "max_positions",
        "text": "return {\"mode\": \"UNCLASSIFIED_DEFENSIVE\", \"max_positions\": 0, \"max_total_exposure_pct\": 0.0}",
        "context": [
          {
            "line": 835,
            "text": "            return {\"mode\": \"DOWNTREND_DEFENSIVE\", \"max_positions\": 1, \"max_total_exposure_pct\": 10.0}"
          },
          {
            "line": 836,
            "text": "        if regime == \"N/A\":"
          },
          {
            "line": 837,
            "text": "            return {\"mode\": \"N/A\", \"max_positions\": None, \"max_total_exposure_pct\": None}"
          },
          {
            "line": 838,
            "text": "        return {\"mode\": \"UNCLASSIFIED_DEFENSIVE\", \"max_positions\": 0, \"max_total_exposure_pct\": 0.0}"
          },
          {
            "line": 839,
            "text": ""
          },
          {
            "line": 840,
            "text": "    def _e1r_dominant_regime(weights: dict) -> str:"
          },
          {
            "line": 841,
            "text": "        if not weights:"
          }
        ]
      },
      {
        "line": 845,
        "keyword": "entry_top_n",
        "text": "entry_top_n = int(a.get(\"entry_top_n\", 3))",
        "context": [
          {
            "line": 842,
            "text": "            return \"UNCLASSIFIED\" if e1r_regime_wiring_enabled else \"N/A\""
          },
          {
            "line": 843,
            "text": "        return max(weights.items(), key=lambda kv: kv[1])[0]"
          },
          {
            "line": 844,
            "text": ""
          },
          {
            "line": 845,
            "text": "    entry_top_n = int(a.get(\"entry_top_n\", 3))"
          },
          {
            "line": 846,
            "text": "    rank_based_exit = bool(a.get(\"rank_based_exit\", False))"
          },
          {
            "line": 847,
            "text": "    market_gate_enabled = bool(a.get(\"market_gate_enabled\", True))"
          },
          {
            "line": 848,
            "text": "    risk_off_below_spx_ma50 = bool(a.get(\"risk_off_below_spx_ma50\", True))"
          }
        ]
      },
      {
        "line": 852,
        "keyword": "candidate_top_n",
        "text": "candidate_top_n           = a.get(\"candidate_top_n\", None)   # None = 沿用旧 entry_top_n",
        "context": [
          {
            "line": 849,
            "text": "    ls60_exit_mode = a.get(\"ls60_exit_mode\", \"reduce\")  # \"exit\"=旧规则 \"reduce\"=新规则"
          },
          {
            "line": 850,
            "text": ""
          },
          {
            "line": 851,
            "text": "    # Qualified Candidate Pool 参数"
          },
          {
            "line": 852,
            "text": "    candidate_top_n           = a.get(\"candidate_top_n\", None)   # None = 沿用旧 entry_top_n"
          },
          {
            "line": 853,
            "text": "    qualified_entry_enabled   = bool(a.get(\"qualified_entry_enabled\", False))"
          },
          {
            "line": 854,
            "text": "    qualified_rs_min          = float(a.get(\"qualified_rs_min\", 90.0))"
          },
          {
            "line": 855,
            "text": "    qualified_momentum_min    = float(a.get(\"qualified_momentum_min\", 85.0))"
          }
        ]
      },
      {
        "line": 852,
        "keyword": "entry_top_n",
        "text": "candidate_top_n           = a.get(\"candidate_top_n\", None)   # None = 沿用旧 entry_top_n",
        "context": [
          {
            "line": 849,
            "text": "    ls60_exit_mode = a.get(\"ls60_exit_mode\", \"reduce\")  # \"exit\"=旧规则 \"reduce\"=新规则"
          },
          {
            "line": 850,
            "text": ""
          },
          {
            "line": 851,
            "text": "    # Qualified Candidate Pool 参数"
          },
          {
            "line": 852,
            "text": "    candidate_top_n   
```

## Conclusion
- `ENTRYPOINTS_IDENTIFIED_BUT_COMBINED_ADAPTER_STILL_NEEDS_EXPLICIT_NO_STRATEGY_CHANGE_GUARDS`
- Recommended: Create 4C-2C-4C adapter dry-run/smoke that calls these original entrypoints only, enforces global holdings <=3, and reports branch usage before full 5Y run.

