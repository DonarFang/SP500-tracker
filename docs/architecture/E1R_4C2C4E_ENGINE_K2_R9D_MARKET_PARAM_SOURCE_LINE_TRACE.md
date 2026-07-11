# E1R 4C-2C-4E-ENGINE-K2-R9D — Market Parameter Source-Line Trace

Generated At: `2026-07-11T03:15:59.972384+00:00`

## Purpose
Trace clean source-line/source-head evidence for each required 115% E1R market gate parameter and call-chain field.

## Target Artifact
```json
{
  "exists": true,
  "path": "exports/e1r_v0_2_backtest_summary.json",
  "sha256": "449a8ace55ce2335d174e17e2532d8793a3a9b99c021a935f8d7f2e531092114",
  "selected_fields": {
    "strategy_id": "E1R_REGIME_AWARE_V0_2",
    "total_return_pct": 116.7435999134756,
    "spx_return_pct": 76.844174428316,
    "alpha_pct": 39.89942548515961,
    "max_drawdown_pct": 25.904809362815108,
    "profit_factor": 1.1919630955509348,
    "sharpe_ratio": 0.7957270568329264,
    "regime_aware_logic": "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE",
    "sidecar_active_by_regime": {
      "SIDEWAYS": 135
    },
    "sidecar_active_by_subclass": {
      "MA_CONFLICT": 135
    },
    "variant": "E1R_REGIME_AWARE_V0_2",
    "source_file": "exports/e1r_v0_2_backtest_summary.json"
  }
}
```

## Source Filter
```json
{
  "primary_source_files": [
    "src/engine/backtest.py",
    "src/engine/e1r_composer.py",
    "src/engine/e1r_sidecar_sleeve.py"
  ],
  "trace_candidate_paths_count": 146,
  "trace_candidate_paths_sample": [
    "docs/research/E1R_V0_2_STAGE3_8E2F2C4C4_GENERATOR_INTERNALS_EXPORT_WRAPPER_PROTOTYPE.json",
    "docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json",
    "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0_E1_E1R_CORE_CONTRACT_AUDIT.json",
    "exports/e1_5y_backtest_equity_curve.json",
    "exports/e1r_v0_2_sidecar_records_5y.json",
    "docs/research/E1R_V0_2_STAGE3_8E2F2C4C2_RECOVER_5Y_PORTFOLIO_EQUITY_CANDIDATES.json",
    "docs/research/E1R_V0_2_STAGE3_8E2F1E0_TARGET_ACTION_INPUT_AUDIT.json",
    "scripts/run_e1r_v0_2_oos.py",
    "docs/research/E1R_V0_2_STAGE3_8E2F1A_FORWARD_SOURCE_AUDIT.json",
    "docs/research/E1R_V0_2_STAGE3_8E2F2C4C3_BACKTEST_GENERATOR_CANONICAL_EXPORT_PLAN.json",
    "exports/e1r_v0_2_portfolio_backtest_equity_curve.json",
    "exports/e1_e1r_5y_equity_comparison.json",
    "exports/e1r_v0_2_backtest_equity_curve.json",
    "exports/portfolio_backtest.json",
    "exports/backtest.json",
    "exports/e1r_v0_2_backtest_summary.json",
    "exports/oos_e1r_v0_2_equity_curve.json",
    "exports/oos_equity_curve.json",
    "scripts/run_e1r_v0_2_oos_equity.py",
    "scripts/run_e1r_v0_2_forward_performance.py",
    "scripts/export_e1r_v0_2_status.py",
    "scripts/run_e1r_v0_2_sidecar_lifecycle.py",
    "src/engine/e1r_composer.py",
    "src/engine/e1r_sidecar_sleeve.py",
    "src/oos/tracking_engine.py",
    "src/oos/portfolio_state.py",
    "src/oos/exporter.py",
    "exports/e1r_v0_2_status.json",
    "exports/oos_e1r_v0_2_summary.json",
    "exports/oos_e1r_v0_2_positions.json",
    "exports/oos_e1r_v0_2_orders.json",
    "exports/oos_e1r_v0_2_sidecar.json",
    "exports/oos_e1r_v0_2_sidecar_lifecycle.json",
    "exports/oos_e1r_v0_2_sidecar_turnover.json",
    "exports/leaderboard.json",
    "exports/market_state.json",
    "docs/research/E1R_V0_2_STAGE3_8E2F0_FORWARD_KICKOFF_AUDIT.json",
    "exports/oos_summary.json",
    "docs/research/stage3_2_backtest_snapshots/backtest_main_before_stage3_2.py",
    "scripts/export_e1r_v0_2_backtest_equity.py",
    "src/engine/backtest.py",
    "src/oos/__init__.py",
    "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0_E1_E1R_CORE_CONTRACT_AUDIT.md",
    "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0B_E1R_CORE_VARIANT_SOURCE_RECOVERY.json",
    "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F3D_E1_CANONICAL_INTEGRITY_AUDIT.json",
    "docs/research/E1R_V0_2_STAGE3_8E2F2C4C8_DRY_RUN_GENERATION_PATH_AUDIT.json",
    "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F3C_E1_CORE_EXPORT_REPORT.json",
    "docs/research/E1R_V0_2_STAGE3_8E2F2C4C5_EXPORT_WRAPPER_SMOKE_REPORT.json",
    "docs/research/E1R_V0_2_STAGE3_5_ARTIFACT_DISCOVERY_REPORT.json",
    "docs/research/E1R_V0_2_STAGE3_8E2F2C4A1_SIDECAR_ACTIVATION_AUDIT.json"
  ],
  "polluted_prefixes_excluded_as_primary_proof": [
    "docs/research/E1R_4C2C4E_ENGINE_K2_",
    "docs/architecture/E1R_4C2C4E_ENGINE_K2_",
    "exports/e1r_engine/audit/",
    "exports/e1r_engine/equivalence/",
    "scripts/e1r_k2_r9",
    "scripts/e1r_k2_rca"
  ],
  "preferred_original_trace_prefixes": [
    "docs/research/E1R_V0_2_STAGE3_",
    "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_"
  ]
}
```

## Evidence Matrix
```json
{
  "market_gate_enabled": {
    "status": "PASS",
    "clean_evidence_count": 29,
    "primary_source_count": 3,
    "original_trace_or_source_head_count": 26,
    "polluted_evidence_count": 0,
    "best_evidence": [
      {
        "field": "market_gate_enabled",
        "source_path": "src/engine/backtest.py",
        "source_class": "PRIMARY_SOURCE_CODE",
        "line": 847,
        "matched_pattern": "market_gate_enabled\\s*=\\s*bool\\(a\\.get\\(\"market_gate_enabled\"",
        "line_text": "    market_gate_enabled = bool(a.get(\"market_gate_enabled\", True))",
        "context": [
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
          },
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
          }
        ]
      },
      {
        "field": "market_gate_enabled",
        "source_path": "src/engine/backtest.py",
        "source_class": "PRIMARY_SOURCE_CODE",
        "line": 2526,
        "matched_pattern": "\"market_gate_enabled\"\\s*:\\s*True",
        "line_text": "        \"market_gate_enabled\":       True,",
        "context": [
          {
            "line": 2522,
            "text": "        \"block_add_after_take_profit\": False,"
          },
          {
            "line": 2523,
            "text": "    }"
          },
          {
            "line": 2524,
            "text": "    # ── Gate v2 No VIX（冻结市场层基准）─────────────────────────"
          },
          {
            "line": 2525,
            "text": "    _gate_v2_no_vix = {"
          },
          {
            "line": 2526,
            "text": "        \"market_gate_enabled\":       True,"
          },
          {
            "line": 2527,
            "text": "        \"risk_off_below_spx_ma50\":   True,"
          },
          {
            "line": 2528,
            "text": "        \"market_shock_gate_enabled\": True,"
          },
          {
            "line": 2529,
            "text": "        \"market_shock_daily_return\": -0.02,"
          },
          {
            "line": 2530,
            "text": "        \"candidate_top_n\":           None,"
          }
        ]
      },
      {
        "field": "market_gate_enabled",
        "source_path": "src/engine/backtest.py",
        "source_class": "PRIMARY_SOURCE_CODE",
        "line": 2537,
        "matched_pattern": "\"market_gate_enabled\"\\s*:\\s*True",
        "line_text": "        \"market_gate_enabled\":       True,",
        "context": [
          {
            "line": 2533,
            "text": "    }"
          },
          {
            "line": 2534,
            "text": ""
          },
          {
            "line": 2535,
            "text": "    # ── E2 实验配置（Gate 固定 G4，只改退出层）────────────────"
          },
          {
            "line": 2536,
            "text": "    _gate_g4 = {"
          },
          {
            "line": 2537,
            "text": "        \"market_gate_enabled\":       True,"
          },
          {
            "line": 2538,
            "text": "        \"risk_off_below_spx_ma50\":   False,"
          },
          {
            "line": 2539,
            "text": "        \"market_shock_gate_enabled\": False,"
          },
          {
            "line": 2540,
            "text": "        \"market_shock_daily_return\": -0.02,"
          },
          {
            "line": 2541,
            "text": "        \"gate_use_slope\":            True,"
          }
        ]
      },
      "{\"field\": \"market_gate_enabled\", \"source_path\": \"docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json\", \"source_class\": \"ORIGINAL_TRACE_OR_SOURCE_HEAD_ARTIFACT\", \"json_path\": \"source_file_reports.src/engine/backtest.py.functions[3].source_head\", \"matched_pattern\": \"\\\"market_gate_enabled\\\"\\\\s*:\\\\s*True\", \"line_text\": \"def run_strategy_variant_comparison(\\n    symbols: list[str],\\n    prices_map: dict[str, list[float]],\\n    dates_map: dict[str, list[str]],\\n    spx_prices: list[float],\\n    spx_dates: list[str],\\n    ndx_prices: list[float] = None,\\n    ndx_dates:  list[str]   = None,\\n    sox_prices: list[float] = None,\\n    sox_dates:  list[str]   = None,\\n    vix_prices: list[float] = None,\\n    vix_dates:  list[str]   = None,\\n) -> dict:\\n    \\\"\\\"\\\"\\n    Run four diagnostic portfolio variants using Strict Top3, no fixed TP.\\n\\n    V0_BASE: current Strict Top3 baseline.\\n    V1_RS95: raise entry RS threshold from 90 to 95.\\n    V2_RS95_MINHOLD5: add minimum 5 trading-day hold for ordinary REDUCE/EXIT.\\n    V3_RS95_MINHOLD5_RELSTOP8: add relative SPX underperformance stop.\\n\\n    Selection policy:\\n    1. Prefer PASS over PARTIAL over FAIL.\\n    2. Within the same status, prefer higher total return.\\n    3. Break ties with higher Profit Factor, higher Sharpe, then lower max drawdown.\\n    \\\"\\\"\\\"\\n    logger.info(\\\"[Backtest Layer D v1.6] Strategy Variant Comparison...\\\")\\n\\n    base = {\\n        **LAYER_D_ASSUMPTIONS,\\n        \\\"market_gate_enabled\\\": False,\\n        \\\"market_shock_gate_enabled\\\": False,\\n        \\\"partial_take_profit_enabled\\\": False,\\n        \\\"block_add_after_take_profit\\\": False,\\n    }\\n    # ── Gate v2 No VIX（冻结市场层基准）─────────────────────────\\n    _gate_v2_no_vix = {\\n        \\\"market_gate_enabled\\\":       True,\\n        \\\"risk_off_below_spx_ma50\\\":   True,\\n        \\\"market_shock_gate_enabled\\\": True,\\n        \\\"market_shock_daily_return\\\": -0.02,\\n        \\\"candidate_top_n\\\":           None,\\n        \\\"qualified_entry_enabled\\\":   False,\\n        \\\"fill_only_enabled\\\":         False,\\n    }\\n\\n    # ── E2 实验配置（Gate 固定 G4，只改退出层）────────────────\\n    _gate_g4 = {\\n        \\\"market_gate_enabled\\\":       True,\\n        \\\"risk_off_below_spx_ma50\\\":   False,\\n        \\\"market_shock_gate_enabled\\\": False,\\n        \\\"market_shock_daily_return\\\": -0.02,\\n        \\\"gate_use_slope\\\":            True,\\n        \\\"gate_use...<truncated>",
      {
        "field": "market_gate_enabled",
        "source_path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0_E1_E1R_CORE_CONTRACT_AUDIT.json",
        "source_class": "ORIGINAL_TRACE_OR_SOURCE_HEAD_ARTIFACT",
        "json_path": "source_hits.src/engine/backtest.py[11].context[0].text",
        "matched_pattern": "market_gate_enabled\\s*=\\s*bool\\(a\\.get\\(\"market_gate_enabled\"",
        "line_text": "    market_gate_enabled = bool(a.get(\"market_gate_enabled\", True))",
        "context": []
      },
      "{\"field\": \"market_gate_enabled\", \"source_path\": \"docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0_E1_E1R_CORE_CONTRACT_AUDIT.json\", \"source_class\": \"ORIGINAL_TRACE_OR_SOURCE_HEAD_ARTIFACT\", \"json_path\": \"function_sources.src/engine/backtest.py.run_stateful_simulation.source\", \"matched_pattern\": \"market_gate_enabled\\\\s*=\\\\s*bool\\\\(a\\\\.get\\\\(\\\"market_gate_enabled\\\"\", \"line_text\": \"def run_stateful_simulation(\\n    symbols:        list[str],\\n    prices_map:     dict[str, list[float]],\\n    dates_map:      dict[str, list[str]],\\n    spx_prices:     list[float],\\n    spx_dates:      list[str],\\n    ohlc_map:       dict = None,\\n    assumptions:    dict = None,\\n    step:           int  = 1,\\n    min_history:    int  = 120,\\n    market_score_default: float = 60.0,\\n    sim_start_date: str  = None,  # 交易执行起始日（None=从 min_history 后开始）\\n    sim_end_date:   str  = None,  # 交易执行截止日（None=到末尾）\\n    ndx_prices:     list = None,  # NDX 收盘价（Gate v2 Leadership 判断）\\n    ndx_dates:      list = None,\\n    sox_prices:     list = None,  # SOX 收盘价\\n    sox_dates:      list = None,\\n    vix_prices:     list = None,  # VIX 收盘价\\n    vix_dates:      list = None,\\n) -> dict:\\n    \\\"\\\"\\\"\\n    Layer D v1.6: Strict Top3 + RS threshold + MinHold + Relative SPX Stop\\n\\n    修正项（相比 v3）：\\n    1. SPX master calendar — 时间轴以 SPX dates 为准\\n    2. Date-based alignment — 所有股票按日期查找，不用 index 直接对齐\\n    3. skipped_orders_by_reason — 跳过原因分类统计\\n    4. sample_validity 检查 — 样本不足时返回 INSUFFICIENT_SAMPLE\\n    \\\"\\\"\\\"\\n    logger.info(\\\"[Backtest Layer D v1.6] Strict Top3 + RS/MinHold/RelStop Backtest...\\\")\\n\\n    # ── 冻结参数 ─────────────────────────────────────────\\n    a        = assumptions or LAYER_D_ASSUMPTIONS\\n    max_pos  = a[\\\"max_positions\\\"]\\n    buy_pct  = a[\\\"buy_size\\\"]  / max_pos       # Top3: 1/3 per full slot\\n    add_pct  = a[\\\"add_size\\\"]  / max_pos       # Top3: +1/6, only useful after REDUCE\\n    max_pct  = a[\\\"max_single_size\\\"] / max_pos # Top3: max 1/3 per position\\n    one_way  = a[\\\"total_one_way\\\"]             # 0.001\\n    init_cap = float(a.get(\\\"initial_capital\\\", 100_000))\\n    strategy_variant = a.get(\\\"strategy_variant\\\", \\\"top3_entry_rs_minhold_relstop\\\")\\n    e1r_shell_mode = bool(a.get(\\\"e1r_shell_mode\\\", False))\\n    e1r_regime_wiring_enabled = bool(a.get(\\\"e1r_regime_wiring_enabled\\\", False))\\n    e1r_uptrend_execution_enabled = bool(a.get(\\\"e1r_uptrend_execution_enabled\\\", False)...<truncated>",
      "{\"field\": \"market_gate_enabled\", \"source_path\": \"docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0_E1_E1R_CORE_CONTRACT_AUDIT.json\", \"source_class\": \"ORIGINAL_TRACE_OR_SOURCE_HEAD_ARTIFACT\", \"json_path\": \"function_sources.src/engine/backtest.py.run_strategy_variant_comparison.source\", \"matched_pattern\": \"\\\"market_gate_enabled\\\"\\\\s*:\\\\s*True\", \"line_text\": \"def run_strategy_variant_comparison(\\n    symbols: list[str],\\n    prices_map: dict[str, list[float]],\\n    dates_map: dict[str, list[str]],\\n    spx_prices: list[float],\\n    spx_dates: list[str],\\n    ndx_prices: list[float] = None,\\n    ndx_dates:  list[str]   = None,\\n    sox_prices: list[float] = None,\\n    sox_dates:  list[str]   = None,\\n    vix_prices: list[float] = None,\\n    vix_dates:  list[str]   = None,\\n) -> dict:\\n    \\\"\\\"\\\"\\n    Run four diagnostic portfolio variants using Strict Top3, no fixed TP.\\n\\n    V0_BASE: current Strict Top3 baseline.\\n    V1_RS95: raise entry RS threshold from 90 to 95.\\n    V2_RS95_MINHOLD5: add minimum 5 trading-day hold for ordinary REDUCE/EXIT.\\n    V3_RS95_MINHOLD5_RELSTOP8: add relative SPX underperformance stop.\\n\\n    Selection policy:\\n    1. Prefer PASS over PARTIAL over FAIL.\\n    2. Within the same status, prefer higher total return.\\n    3. Break ties with higher Profit Factor, higher Sharpe, then lower max drawdown.\\n    \\\"\\\"\\\"\\n    logger.info(\\\"[Backtest Layer D v1.6] Strategy Variant Comparison...\\\")\\n\\n    base = {\\n        **LAYER_D_ASSUMPTIONS,\\n        \\\"market_gate_enabled\\\": False,\\n        \\\"market_shock_gate_enabled\\\": False,\\n        \\\"partial_take_profit_enabled\\\": False,\\n        \\\"block_add_after_take_profit\\\": False,\\n    }\\n    # ── Gate v2 No VIX（冻结市场层基准）─────────────────────────\\n    _gate_v2_no_vix = {\\n        \\\"market_gate_enabled\\\":       True,\\n        \\\"risk_off_below_spx_ma50\\\":   True,\\n        \\\"market_shock_gate_enabled\\\": True,\\n        \\\"market_shock_daily_return\\\": -0.02,\\n        \\\"candidate_top_n\\\":           None,\\n        \\\"qualified_entry_enabled\\\":   False,\\n        \\\"fill_only_enabled\\\":         False,\\n    }\\n\\n    # ── E2 实验配置（Gate 固定 G4，只改退出层）────────────────\\n    _gate_g4 = {\\n        \\\"market_gate_enabled\\\":       True,\\n        \\\"risk_off_below_spx_ma50\\\":   False,\\n        \\\"market_shock_gate_enabled\\\": False,\\n        \\\"market_shock_daily_return\\\": -0.02,\\n        \\\"gate_use_slope\\\":            True,\\n       ...<truncated>",
      {
        "field": "market_gate_enabled",
        "source_path": "docs/research/E1R_V0_2_STAGE3_8E2F1A_FORWARD_SOURCE_AUDIT.json",
        "source_class": "ORIGINAL_TRACE_OR_SOURCE_HEAD_ARTIFACT",
        "json_path": "source_reports.src/engine/backtest.py.line_hits[17].text",
        "matched_pattern": "market_gate_enabled\\s*=\\s*bool\\(a\\.get\\(\"market_gate_enabled\"",
        "line_text": "    market_gate_enabled = bool(a.get(\"market_gate_enabled\", True))",
        "context": []
      },
      {
        "field": "market_gate_enabled",
        "source_path": "docs/research/E1R_V0_2_STAGE3_8E2F1A_FORWARD_SOURCE_AUDIT.json",
        "source_class": "ORIGINAL_TRACE_OR_SOURCE_HEAD_ARTIFACT",
        "json_path": "source_reports.src/engine/backtest.py.line_hits[90].text",
        "matched_pattern": "\"market_gate_enabled\"\\s*:\\s*True",
        "line_text": "        \"market_gate_enabled\":       True,",
        "context": []
      },
      {
        "field": "market_gate_enabled",
        "source_path": "docs/research/E1R_V0_2_STAGE3_8E2F1A_FORWARD_SOURCE_AUDIT.json",
        "source_class": "ORIGINAL_TRACE_OR_SOURCE_HEAD_ARTIFACT",
        "json_path": "source_reports.src/engine/backtest.py.line_hits[93].text",
        "matched_pattern": "\"market_gate_enabled\"\\s*:\\s*True",
        "line_text": "        \"market_gate_enabled\":       True,",
        "context": []
      },
      {
        "field": "market_gate_enabled",
        "source_path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C3_BACKTEST_GENERATOR_CANONICAL_EXPORT_PLAN.json",
        "source_class": "ORIGINAL_TRACE_OR_SOURCE_HEAD_ARTIFACT",
        "json_path": "important_files.src/engine/backtest.py.hits[22].text",
        "matched_pattern": "market_gate_enabled\\s*=\\s*bool\\(a\\.get\\(\"market_gate_enabled\"",
        "line_text": "    market_gate_enabled = bool(a.get(\"market_gate_enabled\", True))",
        "context": []
      },
      {
        "field": "market_gate_enabled",
        "source_path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C3_BACKTEST_GENERATOR_CANONICAL_EXPORT_PLAN.json",
        "source_class": "ORIGINAL_TRACE_OR_SOURCE_HEAD_ARTIFACT",
        "json_path": "important_files.src/engine/backtest.py.hits[156].text",
        "matched_pattern": "\"market_gate_enabled\"\\s*:\\s*True",
        "line_text": "        \"market_gate_enabled\":       True,",
        "context": []
      }
    ],
    "polluted_examples": [],
    "required": "Assignment/default and call-path into run_stateful_simulation assumptions for E1R v0.2 core."
  },
  "risk_off_below_spx_ma50": {
    "status": "PASS",
    "clean_evidence_count": 20,
    "primary_source_count": 2,
    "original_trace_or_source_head_count": 18,
    "polluted_evidence_count": 0,
    "best_evidence": [
      {
        "field": "risk_off_below_spx_ma50",
        "source_path": "src/engine/backtest.py",
        "source_class": "PRIMARY_SOURCE_CODE",
        "line": 848,
        "matched_pattern": "risk_off_below_spx_ma50\\s*=\\s*bool\\(a\\.get\\(\"risk_off_below_spx_ma50\"",
        "line_text": "    risk_off_below_spx_ma50 = bool(a.get(\"risk_off_below_spx_ma50\", True))",
        "context": [
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
          },
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
          }
        ]
      },
      {
        "field": "risk_off_below_spx_ma50",
        "source_path": "src/engine/backtest.py",
        "source_class": "PRIMARY_SOURCE_CODE",
        "line": 2527,
        "matched_pattern": "\"risk_off_below_spx_ma50\"\\s*:\\s*True",
        "line_text": "        \"risk_off_below_spx_ma50\":   True,",
        "context": [
          {
            "line": 2523,
            "text": "    }"
          },
          {
            "line": 2524,
            "text": "    # ── Gate v2 No VIX（冻结市场层基准）─────────────────────────"
          },
          {
            "line": 2525,
            "text": "    _gate_v2_no_vix = {"
          },
          {
            "line": 2526,
            "text": "        \"market_gate_enabled\":       True,"
          },
          {
            "line": 2527,
            "text": "        \"risk_off_below_spx_ma50\":   True,"
          },
          {
            "line": 2528,
            "text": "        \"market_shock_gate_enabled\": True,"
          },
          {
            "line": 2529,
            "text": "        \"market_shock_daily_return\": -0.02,"
          },
          {
            "line": 2530,
            "text": "        \"candidate_top_n\":           None,"
          },
          {
            "line": 2531,
            "text": "        \"qualified_entry_enabled\":   False,"
          }
        ]
      },
      "{\"field\": \"risk_off_below_spx_ma50\", \"source_path\": \"docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json\", \"source_class\": \"ORIGINAL_TRACE_OR_SOURCE_HEAD_ARTIFACT\", \"json_path\": \"source_file_reports.src/engine/backtest.py.functions[3].source_head\", \"matched_pattern\": \"\\\"risk_off_below_spx_ma50\\\"\\\\s*:\\\\s*True\", \"line_text\": \"def run_strategy_variant_comparison(\\n    symbols: list[str],\\n    prices_map: dict[str, list[float]],\\n    dates_map: dict[str, list[str]],\\n    spx_prices: list[float],\\n    spx_dates: list[str],\\n    ndx_prices: list[float] = None,\\n    ndx_dates:  list[str]   = None,\\n    sox_prices: list[float] = None,\\n    sox_dates:  list[str]   = None,\\n    vix_prices: list[float] = None,\\n    vix_dates:  list[str]   = None,\\n) -> dict:\\n    \\\"\\\"\\\"\\n    Run four diagnostic portfolio variants using Strict Top3, no fixed TP.\\n\\n    V0_BASE: current Strict Top3 baseline.\\n    V1_RS95: raise entry RS threshold from 90 to 95.\\n    V2_RS95_MINHOLD5: add minimum 5 trading-day hold for ordinary REDUCE/EXIT.\\n    V3_RS95_MINHOLD5_RELSTOP8: add relative SPX underperformance stop.\\n\\n    Selection policy:\\n    1. Prefer PASS over PARTIAL over FAIL.\\n    2. Within the same status, prefer higher total return.\\n    3. Break ties with higher Profit Factor, higher Sharpe, then lower max drawdown.\\n    \\\"\\\"\\\"\\n    logger.info(\\\"[Backtest Layer D v1.6] Strategy Variant Comparison...\\\")\\n\\n    base = {\\n        **LAYER_D_ASSUMPTIONS,\\n        \\\"market_gate_enabled\\\": False,\\n        \\\"market_shock_gate_enabled\\\": False,\\n        \\\"partial_take_profit_enabled\\\": False,\\n        \\\"block_add_after_take_profit\\\": False,\\n    }\\n    # ── Gate v2 No VIX（冻结市场层基准）─────────────────────────\\n    _gate_v2_no_vix = {\\n        \\\"market_gate_enabled\\\":       True,\\n        \\\"risk_off_below_spx_ma50\\\":   True,\\n        \\\"market_shock_gate_enabled\\\": True,\\n        \\\"market_shock_daily_return\\\": -0.02,\\n        \\\"candidate_top_n\\\":           None,\\n        \\\"qualified_entry_enabled\\\":   False,\\n        \\\"fill_only_enabled\\\":         False,\\n    }\\n\\n    # ── E2 实验配置（Gate 固定 G4，只改退出层）────────────────\\n    _gate_g4 = {\\n        \\\"market_gate_enabled\\\":       True,\\n        \\\"risk_off_below_spx_ma50\\\":   False,\\n        \\\"market_shock_gate_enabled\\\": False,\\n        \\\"market_shock_daily_return\\\": -0.02,\\n        \\\"gate_use_slope\\\":            True,\\n        \\\"...<truncated>",
      {
        "field": "risk_off_below_spx_ma50",
        "source_path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0_E1_E1R_CORE_CONTRACT_AUDIT.json",
        "source_class": "ORIGINAL_TRACE_OR_SOURCE_HEAD_ARTIFACT",
        "json_path": "source_hits.src/engine/backtest.py[11].context[1].text",
        "matched_pattern": "risk_off_below_spx_ma50\\s*=\\s*bool\\(a\\.get\\(\"risk_off_below_spx_ma50\"",
        "line_text": "    risk_off_below_spx_ma50 = bool(a.get(\"risk_off_below_spx_ma50\", True))",
        "context": []
      },
      "{\"field\": \"risk_off_below_spx_ma50\", \"source_path\": \"docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0_E1_E1R_CORE_CONTRACT_AUDIT.json\", \"source_class\": \"ORIGINAL_TRACE_OR_SOURCE_HEAD_ARTIFACT\", \"json_path\": \"function_sources.src/engine/backtest.py.run_stateful_simulation.source\", \"matched_pattern\": \"risk_off_below_spx_ma50\\\\s*=\\\\s*bool\\\\(a\\\\.get\\\\(\\\"risk_off_below_spx_ma50\\\"\", \"line_text\": \"def run_stateful_simulation(\\n    symbols:        list[str],\\n    prices_map:     dict[str, list[float]],\\n    dates_map:      dict[str, list[str]],\\n    spx_prices:     list[float],\\n    spx_dates:      list[str],\\n    ohlc_map:       dict = None,\\n    assumptions:    dict = None,\\n    step:           int  = 1,\\n    min_history:    int  = 120,\\n    market_score_default: float = 60.0,\\n    sim_start_date: str  = None,  # 交易执行起始日（None=从 min_history 后开始）\\n    sim_end_date:   str  = None,  # 交易执行截止日（None=到末尾）\\n    ndx_prices:     list = None,  # NDX 收盘价（Gate v2 Leadership 判断）\\n    ndx_dates:      list = None,\\n    sox_prices:     list = None,  # SOX 收盘价\\n    sox_dates:      list = None,\\n    vix_prices:     list = None,  # VIX 收盘价\\n    vix_dates:      list = None,\\n) -> dict:\\n    \\\"\\\"\\\"\\n    Layer D v1.6: Strict Top3 + RS threshold + MinHold + Relative SPX Stop\\n\\n    修正项（相比 v3）：\\n    1. SPX master calendar — 时间轴以 SPX dates 为准\\n    2. Date-based alignment — 所有股票按日期查找，不用 index 直接对齐\\n    3. skipped_orders_by_reason — 跳过原因分类统计\\n    4. sample_validity 检查 — 样本不足时返回 INSUFFICIENT_SAMPLE\\n    \\\"\\\"\\\"\\n    logger.info(\\\"[Backtest Layer D v1.6] Strict Top3 + RS/MinHold/RelStop Backtest...\\\")\\n\\n    # ── 冻结参数 ─────────────────────────────────────────\\n    a        = assumptions or LAYER_D_ASSUMPTIONS\\n    max_pos  = a[\\\"max_positions\\\"]\\n    buy_pct  = a[\\\"buy_size\\\"]  / max_pos       # Top3: 1/3 per full slot\\n    add_pct  = a[\\\"add_size\\\"]  / max_pos       # Top3: +1/6, only useful after REDUCE\\n    max_pct  = a[\\\"max_single_size\\\"] / max_pos # Top3: max 1/3 per position\\n    one_way  = a[\\\"total_one_way\\\"]             # 0.001\\n    init_cap = float(a.get(\\\"initial_capital\\\", 100_000))\\n    strategy_variant = a.get(\\\"strategy_variant\\\", \\\"top3_entry_rs_minhold_relstop\\\")\\n    e1r_shell_mode = bool(a.get(\\\"e1r_shell_mode\\\", False))\\n    e1r_regime_wiring_enabled = bool(a.get(\\\"e1r_regime_wiring_enabled\\\", False))\\n    e1r_uptrend_execution_enabled = bool(a.get(\\\"e1r_uptrend_execution_enabl...<truncated>",
      "{\"field\": \"risk_off_below_spx_ma50\", \"source_path\": \"docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0_E1_E1R_CORE_CONTRACT_AUDIT.json\", \"source_class\": \"ORIGINAL_TRACE_OR_SOURCE_HEAD_ARTIFACT\", \"json_path\": \"function_sources.src/engine/backtest.py.run_strategy_variant_comparison.source\", \"matched_pattern\": \"\\\"risk_off_below_spx_ma50\\\"\\\\s*:\\\\s*True\", \"line_text\": \"def run_strategy_variant_comparison(\\n    symbols: list[str],\\n    prices_map: dict[str, list[float]],\\n    dates_map: dict[str, list[str]],\\n    spx_prices: list[float],\\n    spx_dates: list[str],\\n    ndx_prices: list[float] = None,\\n    ndx_dates:  list[str]   = None,\\n    sox_prices: list[float] = None,\\n    sox_dates:  list[str]   = None,\\n    vix_prices: list[float] = None,\\n    vix_dates:  list[str]   = None,\\n) -> dict:\\n    \\\"\\\"\\\"\\n    Run four diagnostic portfolio variants using Strict Top3, no fixed TP.\\n\\n    V0_BASE: current Strict Top3 baseline.\\n    V1_RS95: raise entry RS threshold from 90 to 95.\\n    V2_RS95_MINHOLD5: add minimum 5 trading-day hold for ordinary REDUCE/EXIT.\\n    V3_RS95_MINHOLD5_RELSTOP8: add relative SPX underperformance stop.\\n\\n    Selection policy:\\n    1. Prefer PASS over PARTIAL over FAIL.\\n    2. Within the same status, prefer higher total return.\\n    3. Break ties with higher Profit Factor, higher Sharpe, then lower max drawdown.\\n    \\\"\\\"\\\"\\n    logger.info(\\\"[Backtest Layer D v1.6] Strategy Variant Comparison...\\\")\\n\\n    base = {\\n        **LAYER_D_ASSUMPTIONS,\\n        \\\"market_gate_enabled\\\": False,\\n        \\\"market_shock_gate_enabled\\\": False,\\n        \\\"partial_take_profit_enabled\\\": False,\\n        \\\"block_add_after_take_profit\\\": False,\\n    }\\n    # ── Gate v2 No VIX（冻结市场层基准）─────────────────────────\\n    _gate_v2_no_vix = {\\n        \\\"market_gate_enabled\\\":       True,\\n        \\\"risk_off_below_spx_ma50\\\":   True,\\n        \\\"market_shock_gate_enabled\\\": True,\\n        \\\"market_shock_daily_return\\\": -0.02,\\n        \\\"candidate_top_n\\\":           None,\\n        \\\"qualified_entry_enabled\\\":   False,\\n        \\\"fill_only_enabled\\\":         False,\\n    }\\n\\n    # ── E2 实验配置（Gate 固定 G4，只改退出层）────────────────\\n    _gate_g4 = {\\n        \\\"market_gate_enabled\\\":       True,\\n        \\\"risk_off_below_spx_ma50\\\":   False,\\n        \\\"market_shock_gate_enabled\\\": False,\\n        \\\"market_shock_daily_return\\\": -0.02,\\n        \\\"gate_use_slope\\\":            True,\\...<truncated>",
      "{\"field\": \"risk_off_below_spx_ma50\", \"source_path\": \"docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F2_E1_BACKTEST_ENTRY_AUDIT.json\", \"source_class\": \"ORIGINAL_TRACE_OR_SOURCE_HEAD_ARTIFACT\", \"json_path\": \"source_report.functions[0].source_head\", \"matched_pattern\": \"risk_off_below_spx_ma50\\\\s*=\\\\s*bool\\\\(a\\\\.get\\\\(\\\"risk_off_below_spx_ma50\\\"\", \"line_text\": \"def run_stateful_simulation(\\n    symbols:        list[str],\\n    prices_map:     dict[str, list[float]],\\n    dates_map:      dict[str, list[str]],\\n    spx_prices:     list[float],\\n    spx_dates:      list[str],\\n    ohlc_map:       dict = None,\\n    assumptions:    dict = None,\\n    step:           int  = 1,\\n    min_history:    int  = 120,\\n    market_score_default: float = 60.0,\\n    sim_start_date: str  = None,  # 交易执行起始日（None=从 min_history 后开始）\\n    sim_end_date:   str  = None,  # 交易执行截止日（None=到末尾）\\n    ndx_prices:     list = None,  # NDX 收盘价（Gate v2 Leadership 判断）\\n    ndx_dates:      list = None,\\n    sox_prices:     list = None,  # SOX 收盘价\\n    sox_dates:      list = None,\\n    vix_prices:     list = None,  # VIX 收盘价\\n    vix_dates:      list = None,\\n) -> dict:\\n    \\\"\\\"\\\"\\n    Layer D v1.6: Strict Top3 + RS threshold + MinHold + Relative SPX Stop\\n\\n    修正项（相比 v3）：\\n    1. SPX master calendar — 时间轴以 SPX dates 为准\\n    2. Date-based alignment — 所有股票按日期查找，不用 index 直接对齐\\n    3. skipped_orders_by_reason — 跳过原因分类统计\\n    4. sample_validity 检查 — 样本不足时返回 INSUFFICIENT_SAMPLE\\n    \\\"\\\"\\\"\\n    logger.info(\\\"[Backtest Layer D v1.6] Strict Top3 + RS/MinHold/RelStop Backtest...\\\")\\n\\n    # ── 冻结参数 ─────────────────────────────────────────\\n    a        = assumptions or LAYER_D_ASSUMPTIONS\\n    max_pos  = a[\\\"max_positions\\\"]\\n    buy_pct  = a[\\\"buy_size\\\"]  / max_pos       # Top3: 1/3 per full slot\\n    add_pct  = a[\\\"add_size\\\"]  / max_pos       # Top3: +1/6, only useful after REDUCE\\n    max_pct  = a[\\\"max_single_size\\\"] / max_pos # Top3: max 1/3 per position\\n    one_way  = a[\\\"total_one_way\\\"]             # 0.001\\n    init_cap = float(a.get(\\\"initial_capital\\\", 100_000))\\n    strategy_variant = a.get(\\\"strategy_variant\\\", \\\"top3_entry_rs_minhold_relstop\\\")\\n    e1r_shell_mode = bool(a.get(\\\"e1r_shell_mode\\\", False))\\n    e1r_regime_wiring_enabled = bool(a.get(\\\"e1r_regime_wiring_enabled\\\", False))\\n    e1r_uptrend_execution_enabled = bool(a.get(\\\"e1r_uptrend_execution_enabled\\\", False))\\n    e1r_regime_daily =...<truncated>",
      "{\"field\": \"risk_off_below_spx_ma50\", \"source_path\": \"docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F2_E1_BACKTEST_ENTRY_AUDIT.json\", \"source_class\": \"ORIGINAL_TRACE_OR_SOURCE_HEAD_ARTIFACT\", \"json_path\": \"source_report.functions[1].source_head\", \"matched_pattern\": \"\\\"risk_off_below_spx_ma50\\\"\\\\s*:\\\\s*True\", \"line_text\": \"def run_strategy_variant_comparison(\\n    symbols: list[str],\\n    prices_map: dict[str, list[float]],\\n    dates_map: dict[str, list[str]],\\n    spx_prices: list[float],\\n    spx_dates: list[str],\\n    ndx_prices: list[float] = None,\\n    ndx_dates:  list[str]   = None,\\n    sox_prices: list[float] = None,\\n    sox_dates:  list[str]   = None,\\n    vix_prices: list[float] = None,\\n    vix_dates:  list[str]   = None,\\n) -> dict:\\n    \\\"\\\"\\\"\\n    Run four diagnostic portfolio variants using Strict Top3, no fixed TP.\\n\\n    V0_BASE: current Strict Top3 baseline.\\n    V1_RS95: raise entry RS threshold from 90 to 95.\\n    V2_RS95_MINHOLD5: add minimum 5 trading-day hold for ordinary REDUCE/EXIT.\\n    V3_RS95_MINHOLD5_RELSTOP8: add relative SPX underperformance stop.\\n\\n    Selection policy:\\n    1. Prefer PASS over PARTIAL over FAIL.\\n    2. Within the same status, prefer higher total return.\\n    3. Break ties with higher Profit Factor, higher Sharpe, then lower max drawdown.\\n    \\\"\\\"\\\"\\n    logger.info(\\\"[Backtest Layer D v1.6] Strategy Variant Comparison...\\\")\\n\\n    base = {\\n        **LAYER_D_ASSUMPTIONS,\\n        \\\"market_gate_enabled\\\": False,\\n        \\\"market_shock_gate_enabled\\\": False,\\n        \\\"partial_take_profit_enabled\\\": False,\\n        \\\"block_add_after_take_profit\\\": False,\\n    }\\n    # ── Gate v2 No VIX（冻结市场层基准）─────────────────────────\\n    _gate_v2_no_vix = {\\n        \\\"market_gate_enabled\\\":       True,\\n        \\\"risk_off_below_spx_ma50\\\":   True,\\n        \\\"market_shock_gate_enabled\\\": True,\\n        \\\"market_shock_daily_return\\\": -0.02,\\n        \\\"candidate_top_n\\\":           None,\\n        \\\"qualified_entry_enabled\\\":   False,\\n        \\\"fill_only_enabled\\\":         False,\\n    }\\n\\n    # ── E2 实验配置（Gate 固定 G4，只改退出层）────────────────\\n    _gate_g4 = {\\n        \\\"market_gate_enabled\\\":       True,\\n        \\\"risk_off_below_spx_ma50\\\":   False,\\n        \\\"market_shock_gate_enabled\\\": False,\\n        \\\"market_shock_daily_return\\\": -0.02,\\n        \\\"gate_use_slope\\\":            True,\\n        \\\"gate_use_leadership\\\":       True,...<truncated>",
      "{\"field\": \"risk_off_below_spx_ma50\", \"source_path\": \"docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F2_E1_BACKTEST_ENTRY_AUDIT.json\", \"source_class\": \"ORIGINAL_TRACE_OR_SOURCE_HEAD_ARTIFACT\", \"json_path\": \"loop_candidates[0].source_head\", \"matched_pattern\": \"risk_off_below_spx_ma50\\\\s*=\\\\s*bool\\\\(a\\\\.get\\\\(\\\"risk_off_below_spx_ma50\\\"\", \"line_text\": \"def run_stateful_simulation(\\n    symbols:        list[str],\\n    prices_map:     dict[str, list[float]],\\n    dates_map:      dict[str, list[str]],\\n    spx_prices:     list[float],\\n    spx_dates:      list[str],\\n    ohlc_map:       dict = None,\\n    assumptions:    dict = None,\\n    step:           int  = 1,\\n    min_history:    int  = 120,\\n    market_score_default: float = 60.0,\\n    sim_start_date: str  = None,  # 交易执行起始日（None=从 min_history 后开始）\\n    sim_end_date:   str  = None,  # 交易执行截止日（None=到末尾）\\n    ndx_prices:     list = None,  # NDX 收盘价（Gate v2 Leadership 判断）\\n    ndx_dates:      list = None,\\n    sox_prices:     list = None,  # SOX 收盘价\\n    sox_dates:      list = None,\\n    vix_prices:     list = None,  # VIX 收盘价\\n    vix_dates:      list = None,\\n) -> dict:\\n    \\\"\\\"\\\"\\n    Layer D v1.6: Strict Top3 + RS threshold + MinHold + Relative SPX Stop\\n\\n    修正项（相比 v3）：\\n    1. SPX master calendar — 时间轴以 SPX dates 为准\\n    2. Date-based alignment — 所有股票按日期查找，不用 index 直接对齐\\n    3. skipped_orders_by_reason — 跳过原因分类统计\\n    4. sample_validity 检查 — 样本不足时返回 INSUFFICIENT_SAMPLE\\n    \\\"\\\"\\\"\\n    logger.info(\\\"[Backtest Layer D v1.6] Strict Top3 + RS/MinHold/RelStop Backtest...\\\")\\n\\n    # ── 冻结参数 ─────────────────────────────────────────\\n    a        = assumptions or LAYER_D_ASSUMPTIONS\\n    max_pos  = a[\\\"max_positions\\\"]\\n    buy_pct  = a[\\\"buy_size\\\"]  / max_pos       # Top3: 1/3 per full slot\\n    add_pct  = a[\\\"add_size\\\"]  / max_pos       # Top3: +1/6, only useful after REDUCE\\n    max_pct  = a[\\\"max_single_size\\\"] / max_pos # Top3: max 1/3 per position\\n    one_way  = a[\\\"total_one_way\\\"]             # 0.001\\n    init_cap = float(a.get(\\\"initial_capital\\\", 100_000))\\n    strategy_variant = a.get(\\\"strategy_variant\\\", \\\"top3_entry_rs_minhold_relstop\\\")\\n    e1r_shell_mode = bool(a.get(\\\"e1r_shell_mode\\\", False))\\n    e1r_regime_wiring_enabled = bool(a.get(\\\"e1r_regime_wiring_enabled\\\", False))\\n    e1r_uptrend_execution_enabled = bool(a.get(\\\"e1r_uptrend_execution_enabled\\\", False))\\n    e1r_regime_daily = a.get(\\...<truncated>",
      "{\"field\": \"risk_off_below_spx_ma50\", \"source_path\": \"docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F2_E1_BACKTEST_ENTRY_AUDIT.json\", \"source_class\": \"ORIGINAL_TRACE_OR_SOURCE_HEAD_ARTIFACT\", \"json_path\": \"loop_candidates[1].source_head\", \"matched_pattern\": \"\\\"risk_off_below_spx_ma50\\\"\\\\s*:\\\\s*True\", \"line_text\": \"def run_strategy_variant_comparison(\\n    symbols: list[str],\\n    prices_map: dict[str, list[float]],\\n    dates_map: dict[str, list[str]],\\n    spx_prices: list[float],\\n    spx_dates: list[str],\\n    ndx_prices: list[float] = None,\\n    ndx_dates:  list[str]   = None,\\n    sox_prices: list[float] = None,\\n    sox_dates:  list[str]   = None,\\n    vix_prices: list[float] = None,\\n    vix_dates:  list[str]   = None,\\n) -> dict:\\n    \\\"\\\"\\\"\\n    Run four diagnostic portfolio variants using Strict Top3, no fixed TP.\\n\\n    V0_BASE: current Strict Top3 baseline.\\n    V1_RS95: raise entry RS threshold from 90 to 95.\\n    V2_RS95_MINHOLD5: add minimum 5 trading-day hold for ordinary REDUCE/EXIT.\\n    V3_RS95_MINHOLD5_RELSTOP8: add relative SPX underperformance stop.\\n\\n    Selection policy:\\n    1. Prefer PASS over PARTIAL over FAIL.\\n    2. Within the same status, prefer higher total return.\\n    3. Break ties with higher Profit Factor, higher Sharpe, then lower max drawdown.\\n    \\\"\\\"\\\"\\n    logger.info(\\\"[Backtest Layer D v1.6] Strategy Variant Comparison...\\\")\\n\\n    base = {\\n        **LAYER_D_ASSUMPTIONS,\\n        \\\"market_gate_enabled\\\": False,\\n        \\\"market_shock_gate_enabled\\\": False,\\n        \\\"partial_take_profit_enabled\\\": False,\\n        \\\"block_add_after_take_profit\\\": False,\\n    }\\n    # ── Gate v2 No VIX（冻结市场层基准）─────────────────────────\\n    _gate_v2_no_vix = {\\n        \\\"market_gate_enabled\\\":       True,\\n        \\\"risk_off_below_spx_ma50\\\":   True,\\n        \\\"market_shock_gate_enabled\\\": True,\\n        \\\"market_shock_daily_return\\\": -0.02,\\n        \\\"candidate_top_n\\\":           None,\\n        \\\"qualified_entry_enabled\\\":   False,\\n        \\\"fill_only_enabled\\\":         False,\\n    }\\n\\n    # ── E2 实验配置（Gate 固定 G4，只改退出层）────────────────\\n    _gate_g4 = {\\n        \\\"market_gate_enabled\\\":       True,\\n        \\\"risk_off_below_spx_ma50\\\":   False,\\n        \\\"market_shock_gate_enabled\\\": False,\\n        \\\"market_shock_daily_return\\\": -0.02,\\n        \\\"gate_use_slope\\\":            True,\\n        \\\"gate_use_leadership\\\":       True,\\n      ...<truncated>",
      "{\"field\": \"risk_off_below_spx_ma50\", \"source_path\": \"docs/research/E1R_V0_2_STAGE3_8E2F2C4C10A_DIRECT_GENERATOR_FUNCTION_AUDIT.json\", \"source_class\": \"ORIGINAL_TRACE_OR_SOURCE_HEAD_ARTIFACT\", \"json_path\": \"target_reports.src/engine/backtest.py.functions[0].source_head\", \"matched_pattern\": \"risk_off_below_spx_ma50\\\\s*=\\\\s*bool\\\\(a\\\\.get\\\\(\\\"risk_off_below_spx_ma50\\\"\", \"line_text\": \"def run_stateful_simulation(\\n    symbols:        list[str],\\n    prices_map:     dict[str, list[float]],\\n    dates_map:      dict[str, list[str]],\\n    spx_prices:     list[float],\\n    spx_dates:      list[str],\\n    ohlc_map:       dict = None,\\n    assumptions:    dict = None,\\n    step:           int  = 1,\\n    min_history:    int  = 120,\\n    market_score_default: float = 60.0,\\n    sim_start_date: str  = None,  # 交易执行起始日（None=从 min_history 后开始）\\n    sim_end_date:   str  = None,  # 交易执行截止日（None=到末尾）\\n    ndx_prices:     list = None,  # NDX 收盘价（Gate v2 Leadership 判断）\\n    ndx_dates:      list = None,\\n    sox_prices:     list = None,  # SOX 收盘价\\n    sox_dates:      list = None,\\n    vix_prices:     list = None,  # VIX 收盘价\\n    vix_dates:      list = None,\\n) -> dict:\\n    \\\"\\\"\\\"\\n    Layer D v1.6: Strict Top3 + RS threshold + MinHold + Relative SPX Stop\\n\\n    修正项（相比 v3）：\\n    1. SPX master calendar — 时间轴以 SPX dates 为准\\n    2. Date-based alignment — 所有股票按日期查找，不用 index 直接对齐\\n    3. skipped_orders_by_reason — 跳过原因分类统计\\n    4. sample_validity 检查 — 样本不足时返回 INSUFFICIENT_SAMPLE\\n    \\\"\\\"\\\"\\n    logger.info(\\\"[Backtest Layer D v1.6] Strict Top3 + RS/MinHold/RelStop Backtest...\\\")\\n\\n    # ── 冻结参数 ─────────────────────────────────────────\\n    a        = assumptions or LAYER_D_ASSUMPTIONS\\n    max_pos  = a[\\\"max_positions\\\"]\\n    buy_pct  = a[\\\"buy_size\\\"]  / max_pos       # Top3: 1/3 per full slot\\n    add_pct  = a[\\\"add_size\\\"]  / max_pos       # Top3: +1/6, only useful after REDUCE\\n    max_pct  = a[\\\"max_single_size\\\"] / max_pos # Top3: max 1/3 per position\\n    one_way  = a[\\\"total_one_way\\\"]             # 0.001\\n    init_cap = float(a.get(\\\"initial_capital\\\", 100_000))\\n    strategy_variant = a.get(\\\"strategy_variant\\\", \\\"top3_entry_rs_minhold_relstop\\\")\\n    e1r_shell_mode = bool(a.get(\\\"e1r_shell_mode\\\", False))\\n    e1r_regime_wiring_enabled = bool(a.get(\\\"e1r_regime_wiring_enabled\\\", False))\\n    e1r_uptrend_execution_enabled = bool(a.get(\\\"e1r_uptrend_execution_enabled\\\", ...<truncated>",
      "{\"field\": \"risk_off_below_spx_ma50\", \"source_path\": \"docs/research/E1R_V0_2_STAGE3_8E2F2C4C10A_DIRECT_GENERATOR_FUNCTION_AUDIT.json\", \"source_class\": \"ORIGINAL_TRACE_OR_SOURCE_HEAD_ARTIFACT\", \"json_path\": \"target_reports.src/engine/backtest.py.functions[1].source_head\", \"matched_pattern\": \"\\\"risk_off_below_spx_ma50\\\"\\\\s*:\\\\s*True\", \"line_text\": \"def run_strategy_variant_comparison(\\n    symbols: list[str],\\n    prices_map: dict[str, list[float]],\\n    dates_map: dict[str, list[str]],\\n    spx_prices: list[float],\\n    spx_dates: list[str],\\n    ndx_prices: list[float] = None,\\n    ndx_dates:  list[str]   = None,\\n    sox_prices: list[float] = None,\\n    sox_dates:  list[str]   = None,\\n    vix_prices: list[float] = None,\\n    vix_dates:  list[str]   = None,\\n) -> dict:\\n    \\\"\\\"\\\"\\n    Run four diagnostic portfolio variants using Strict Top3, no fixed TP.\\n\\n    V0_BASE: current Strict Top3 baseline.\\n    V1_RS95: raise entry RS threshold from 90 to 95.\\n    V2_RS95_MINHOLD5: add minimum 5 trading-day hold for ordinary REDUCE/EXIT.\\n    V3_RS95_MINHOLD5_RELSTOP8: add relative SPX underperformance stop.\\n\\n    Selection policy:\\n    1. Prefer PASS over PARTIAL over FAIL.\\n    2. Within the same status, prefer higher total return.\\n    3. Break ties with higher Profit Factor, higher Sharpe, then lower max drawdown.\\n    \\\"\\\"\\\"\\n    logger.info(\\\"[Backtest Layer D v1.6] Strategy Variant Comparison...\\\")\\n\\n    base = {\\n        **LAYER_D_ASSUMPTIONS,\\n        \\\"market_gate_enabled\\\": False,\\n        \\\"market_shock_gate_enabled\\\": False,\\n        \\\"partial_take_profit_enabled\\\": False,\\n        \\\"block_add_after_take_profit\\\": False,\\n    }\\n    # ── Gate v2 No VIX（冻结市场层基准）─────────────────────────\\n    _gate_v2_no_vix = {\\n        \\\"market_gate_enabled\\\":       True,\\n        \\\"risk_off_below_spx_ma50\\\":   True,\\n        \\\"market_shock_gate_enabled\\\": True,\\n        \\\"market_shock_daily_return\\\": -0.02,\\n        \\\"candidate_top_n\\\":           None,\\n        \\\"qualified_entry_enabled\\\":   False,\\n        \\\"fill_only_enabled\\\":         False,\\n    }\\n\\n    # ── E2 实验配置（Gate 固定 G4，只改退出层）────────────────\\n    _gate_g4 = {\\n        \\\"market_gate_enabled\\\":       True,\\n        \\\"risk_off_below_spx_ma50\\\":   False,\\n        \\\"market_shock_gate_enabled\\\": False,\\n        \\\"market_shock_daily_return\\\": -0.02,\\n        \\\"gate_use_slope\\\":            True,\\n        \\\"gat...<truncated>"
    ],
    "polluted_examples": [],
    "required": "Assignment/default and usage in market_state / entry_capacity / risk-off logic."
  },
  "market_shock_gate_enabled": {
    "status": "PASS",
    "clean_evidence_count": 22,
    "primary_source_count": 2,
    "original_trace_or_source_head_count": 20,
    "polluted_evidence_count": 0,
    "best_evidence": [
      {
        "field": "market_shock_gate_enabled",
        "source_path": "src/engine/backtest.py",
        "source_class": "PRIMARY_SOURCE_CODE",
        "line": 896,
        "matched_pattern": "market_shock_gate_enabled\\s*=\\s*bool\\(a\\.get\\(\"market_shock_gate_enabled\"",
        "line_text": "    market_shock_gate_enabled = bool(a.get(\"market_shock_gate_enabled\", True))",
        "context": [
          {
            "line": 892,
            "text": "    else:"
          },
          {
            "line": 893,
            "text": "        logger.info(f\"  Entry mode: Strict Top{entry_top_n} (legacy)\")"
          },
          {
            "line": 894,
            "text": "    if ls60_exit_mode not in {\"exit\", \"reduce\"}:"
          },
          {
            "line": 895,
            "text": "        raise ValueError(f\"Invalid ls60_exit_mode={ls60_exit_mode!r}; expected 'exit' or 'reduce'\")"
          },
          {
            "line": 896,
            "text": "    market_shock_gate_enabled = bool(a.get(\"market_shock_gate_enabled\", True))"
          },
          {
            "line": 897,
            "text": "    market_shock_daily_return = float(a.get(\"market_shock_daily_return\", -0.02))"
          },
          {
            "line": 898,
            "text": "    take_profit_enabled = bool(a.get(\"partial_take_profit_enabled\", False))"
          },
          {
            "line": 899,
            "text": "    take_profit_threshold = float(a.get(\"partial_take_profit_threshold\", 0.07))"
          },
          {
            "line": 900,
            "text": "    take_profit_fraction = float(a.get(\"partial_take_profit_fraction\", 0.50))"
          }
        ]
      },
      {
        "field": "market_shock_gate_enabled",
        "source_path": "src/engine/backtest.py",
        "source_class": "PRIMARY_SOURCE_CODE",
        "line": 2528,
        "matched_pattern": "\"market_shock_gate_enabled\"\\s*:\\s*True",
        "line_text": "        \"market_shock_gate_enabled\": True,",
        "context": [
          {
            "line": 2524,
            "text": "    # ── Gate v2 No VIX（冻结市场层基准）─────────────────────────"
          },
          {
            "line": 2525,
            "text": "    _gate_v2_no_vix = {"
          },
          {
            "line": 2526,
            "text": "        \"market_gate_enabled\":       True,"
          },
          {
            "line": 2527,
            "text": "        \"risk_off_below_spx_ma50\":   True,"
          },
          {
            "line": 2528,
            "text": "        \"market_shock_gate_enabled\": True,"
          },
          {
            "line": 2529,
            "text": "        \"market_shock_daily_return\": -0.02,"
          },
          {
            "line": 2530,
            "text": "        \"candidate_top_n\":           None,"
          },
          {
            "line": 2531,
            "text": "        \"qualified_entry_enabled\":   False,"
          },
          {
            "line": 2532,
            "text": "        \"fill_only_enabled\":         False,"
          }
        ]
      },
      "{\"field\": \"market_shock_gate_enabled\", \"source_path\": \"docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json\", \"source_class\": \"ORIGINAL_TRACE_OR_SOURCE_HEAD_ARTIFACT\", \"json_path\": \"source_file_reports.src/engine/backtest.py.functions[3].source_head\", \"matched_pattern\": \"\\\"market_shock_gate_enabled\\\"\\\\s*:\\\\s*True\", \"line_text\": \"def run_strategy_variant_comparison(\\n    symbols: list[str],\\n    prices_map: dict[str, list[float]],\\n    dates_map: dict[str, list[str]],\\n    spx_prices: list[float],\\n    spx_dates: list[str],\\n    ndx_prices: list[float] = None,\\n    ndx_dates:  list[str]   = None,\\n    sox_prices: list[float] = None,\\n    sox_dates:  list[str]   = None,\\n    vix_prices: list[float] = None,\\n    vix_dates:  list[str]   = None,\\n) -> dict:\\n    \\\"\\\"\\\"\\n    Run four diagnostic portfolio variants using Strict Top3, no fixed TP.\\n\\n    V0_BASE: current Strict Top3 baseline.\\n    V1_RS95: raise entry RS threshold from 90 to 95.\\n    V2_RS95_MINHOLD5: add minimum 5 trading-day hold for ordinary REDUCE/EXIT.\\n    V3_RS95_MINHOLD5_RELSTOP8: add relative SPX underperformance stop.\\n\\n    Selection policy:\\n    1. Prefer PASS over PARTIAL over FAIL.\\n    2. Within the same status, prefer higher total return.\\n    3. Break ties with higher Profit Factor, higher Sharpe, then lower max drawdown.\\n    \\\"\\\"\\\"\\n    logger.info(\\\"[Backtest Layer D v1.6] Strategy Variant Comparison...\\\")\\n\\n    base = {\\n        **LAYER_D_ASSUMPTIONS,\\n        \\\"market_gate_enabled\\\": False,\\n        \\\"market_shock_gate_enabled\\\": False,\\n        \\\"partial_take_profit_enabled\\\": False,\\n        \\\"block_add_after_take_profit\\\": False,\\n    }\\n    # ── Gate v2 No VIX（冻结市场层基准）─────────────────────────\\n    _gate_v2_no_vix = {\\n        \\\"market_gate_enabled\\\":       True,\\n        \\\"risk_off_below_spx_ma50\\\":   True,\\n        \\\"market_shock_gate_enabled\\\": True,\\n        \\\"market_shock_daily_return\\\": -0.02,\\n        \\\"candidate_top_n\\\":           None,\\n        \\\"qualified_entry_enabled\\\":   False,\\n        \\\"fill_only_enabled\\\":         False,\\n    }\\n\\n    # ── E2 实验配置（Gate 固定 G4，只改退出层）────────────────\\n    _gate_g4 = {\\n        \\\"market_gate_enabled\\\":       True,\\n        \\\"risk_off_below_spx_ma50\\\":   False,\\n        \\\"market_shock_gate_enabled\\\": False,\\n        \\\"market_shock_daily_return\\\": -0.02,\\n        \\\"gate_use_slope\\\":            True,\\n      ...<truncated>",
      {
        "field": "market_shock_gate_enabled",
        "source_path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0_E1_E1R_CORE_CONTRACT_AUDIT.json",
        "source_class": "ORIGINAL_TRACE_OR_SOURCE_HEAD_ARTIFACT",
        "json_path": "source_hits.src/engine/backtest.py[12].context[4].text",
        "matched_pattern": "market_shock_gate_enabled\\s*=\\s*bool\\(a\\.get\\(\"market_shock_gate_enabled\"",
        "line_text": "    market_shock_gate_enabled = bool(a.get(\"market_shock_gate_enabled\", True))",
        "context": []
      },
      {
        "field": "market_shock_gate_enabled",
        "source_path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0_E1_E1R_CORE_CONTRACT_AUDIT.json",
        "source_class": "ORIGINAL_TRACE_OR_SOURCE_HEAD_ARTIFACT",
        "json_path": "source_hits.src/engine/backtest.py[13].context[3].text",
        "matched_pattern": "market_shock_gate_enabled\\s*=\\s*bool\\(a\\.get\\(\"market_shock_gate_enabled\"",
        "line_text": "    market_shock_gate_enabled = bool(a.get(\"market_shock_gate_enabled\", True))",
        "context": []
      },
      "{\"field\": \"market_shock_gate_enabled\", \"source_path\": \"docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0_E1_E1R_CORE_CONTRACT_AUDIT.json\", \"source_class\": \"ORIGINAL_TRACE_OR_SOURCE_HEAD_ARTIFACT\", \"json_path\": \"function_sources.src/engine/backtest.py.run_stateful_simulation.source\", \"matched_pattern\": \"market_shock_gate_enabled\\\\s*=\\\\s*bool\\\\(a\\\\.get\\\\(\\\"market_shock_gate_enabled\\\"\", \"line_text\": \"def run_stateful_simulation(\\n    symbols:        list[str],\\n    prices_map:     dict[str, list[float]],\\n    dates_map:      dict[str, list[str]],\\n    spx_prices:     list[float],\\n    spx_dates:      list[str],\\n    ohlc_map:       dict = None,\\n    assumptions:    dict = None,\\n    step:           int  = 1,\\n    min_history:    int  = 120,\\n    market_score_default: float = 60.0,\\n    sim_start_date: str  = None,  # 交易执行起始日（None=从 min_history 后开始）\\n    sim_end_date:   str  = None,  # 交易执行截止日（None=到末尾）\\n    ndx_prices:     list = None,  # NDX 收盘价（Gate v2 Leadership 判断）\\n    ndx_dates:      list = None,\\n    sox_prices:     list = None,  # SOX 收盘价\\n    sox_dates:      list = None,\\n    vix_prices:     list = None,  # VIX 收盘价\\n    vix_dates:      list = None,\\n) -> dict:\\n    \\\"\\\"\\\"\\n    Layer D v1.6: Strict Top3 + RS threshold + MinHold + Relative SPX Stop\\n\\n    修正项（相比 v3）：\\n    1. SPX master calendar — 时间轴以 SPX dates 为准\\n    2. Date-based alignment — 所有股票按日期查找，不用 index 直接对齐\\n    3. skipped_orders_by_reason — 跳过原因分类统计\\n    4. sample_validity 检查 — 样本不足时返回 INSUFFICIENT_SAMPLE\\n    \\\"\\\"\\\"\\n    logger.info(\\\"[Backtest Layer D v1.6] Strict Top3 + RS/MinHold/RelStop Backtest...\\\")\\n\\n    # ── 冻结参数 ─────────────────────────────────────────\\n    a        = assumptions or LAYER_D_ASSUMPTIONS\\n    max_pos  = a[\\\"max_positions\\\"]\\n    buy_pct  = a[\\\"buy_size\\\"]  / max_pos       # Top3: 1/3 per full slot\\n    add_pct  = a[\\\"add_size\\\"]  / max_pos       # Top3: +1/6, only useful after REDUCE\\n    max_pct  = a[\\\"max_single_size\\\"] / max_pos # Top3: max 1/3 per position\\n    one_way  = a[\\\"total_one_way\\\"]             # 0.001\\n    init_cap = float(a.get(\\\"initial_capital\\\", 100_000))\\n    strategy_variant = a.get(\\\"strategy_variant\\\", \\\"top3_entry_rs_minhold_relstop\\\")\\n    e1r_shell_mode = bool(a.get(\\\"e1r_shell_mode\\\", False))\\n    e1r_regime_wiring_enabled = bool(a.get(\\\"e1r_regime_wiring_enabled\\\", False))\\n    e1r_uptrend_execution_enabled = bool(a.get(\\\"e1r_uptrend_execution...<truncated>",
      "{\"field\": \"market_shock_gate_enabled\", \"source_path\": \"docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0_E1_E1R_CORE_CONTRACT_AUDIT.json\", \"source_class\": \"ORIGINAL_TRACE_OR_SOURCE_HEAD_ARTIFACT\", \"json_path\": \"function_sources.src/engine/backtest.py.run_strategy_variant_comparison.source\", \"matched_pattern\": \"\\\"market_shock_gate_enabled\\\"\\\\s*:\\\\s*True\", \"line_text\": \"def run_strategy_variant_comparison(\\n    symbols: list[str],\\n    prices_map: dict[str, list[float]],\\n    dates_map: dict[str, list[str]],\\n    spx_prices: list[float],\\n    spx_dates: list[str],\\n    ndx_prices: list[float] = None,\\n    ndx_dates:  list[str]   = None,\\n    sox_prices: list[float] = None,\\n    sox_dates:  list[str]   = None,\\n    vix_prices: list[float] = None,\\n    vix_dates:  list[str]   = None,\\n) -> dict:\\n    \\\"\\\"\\\"\\n    Run four diagnostic portfolio variants using Strict Top3, no fixed TP.\\n\\n    V0_BASE: current Strict Top3 baseline.\\n    V1_RS95: raise entry RS threshold from 90 to 95.\\n    V2_RS95_MINHOLD5: add minimum 5 trading-day hold for ordinary REDUCE/EXIT.\\n    V3_RS95_MINHOLD5_RELSTOP8: add relative SPX underperformance stop.\\n\\n    Selection policy:\\n    1. Prefer PASS over PARTIAL over FAIL.\\n    2. Within the same status, prefer higher total return.\\n    3. Break ties with higher Profit Factor, higher Sharpe, then lower max drawdown.\\n    \\\"\\\"\\\"\\n    logger.info(\\\"[Backtest Layer D v1.6] Strategy Variant Comparison...\\\")\\n\\n    base = {\\n        **LAYER_D_ASSUMPTIONS,\\n        \\\"market_gate_enabled\\\": False,\\n        \\\"market_shock_gate_enabled\\\": False,\\n        \\\"partial_take_profit_enabled\\\": False,\\n        \\\"block_add_after_take_profit\\\": False,\\n    }\\n    # ── Gate v2 No VIX（冻结市场层基准）─────────────────────────\\n    _gate_v2_no_vix = {\\n        \\\"market_gate_enabled\\\":       True,\\n        \\\"risk_off_below_spx_ma50\\\":   True,\\n        \\\"market_shock_gate_enabled\\\": True,\\n        \\\"market_shock_daily_return\\\": -0.02,\\n        \\\"candidate_top_n\\\":           None,\\n        \\\"qualified_entry_enabled\\\":   False,\\n        \\\"fill_only_enabled\\\":         False,\\n    }\\n\\n    # ── E2 实验配置（Gate 固定 G4，只改退出层）────────────────\\n    _gate_g4 = {\\n        \\\"market_gate_enabled\\\":       True,\\n        \\\"risk_off_below_spx_ma50\\\":   False,\\n        \\\"market_shock_gate_enabled\\\": False,\\n        \\\"market_shock_daily_return\\\": -0.02,\\n        \\\"gate_use_slope\\\":            Tr...<truncated>",
      {
        "field": "market_shock_gate_enabled",
        "source_path": "docs/research/E1R_V0_2_STAGE3_8E2F1A_FORWARD_SOURCE_AUDIT.json",
        "source_class": "ORIGINAL_TRACE_OR_SOURCE_HEAD_ARTIFACT",
        "json_path": "source_reports.src/engine/backtest.py.line_hits[18].text",
        "matched_pattern": "market_shock_gate_enabled\\s*=\\s*bool\\(a\\.get\\(\"market_shock_gate_enabled\"",
        "line_text": "    market_shock_gate_enabled = bool(a.get(\"market_shock_gate_enabled\", True))",
        "context": []
      },
      {
        "field": "market_shock_gate_enabled",
        "source_path": "docs/research/E1R_V0_2_STAGE3_8E2F1A_FORWARD_SOURCE_AUDIT.json",
        "source_class": "ORIGINAL_TRACE_OR_SOURCE_HEAD_ARTIFACT",
        "json_path": "source_reports.src/engine/backtest.py.line_hits[91].text",
        "matched_pattern": "\"market_shock_gate_enabled\"\\s*:\\s*True",
        "line_text": "        \"market_shock_gate_enabled\": True,",
        "context": []
      },
      {
        "field": "market_shock_gate_enabled",
        "source_path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C3_BACKTEST_GENERATOR_CANONICAL_EXPORT_PLAN.json",
        "source_class": "ORIGINAL_TRACE_OR_SOURCE_HEAD_ARTIFACT",
        "json_path": "important_files.src/engine/backtest.py.hits[23].text",
        "matched_pattern": "market_shock_gate_enabled\\s*=\\s*bool\\(a\\.get\\(\"market_shock_gate_enabled\"",
        "line_text": "    market_shock_gate_enabled = bool(a.get(\"market_shock_gate_enabled\", True))",
        "context": []
      },
      {
        "field": "market_shock_gate_enabled",
        "source_path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C3_BACKTEST_GENERATOR_CANONICAL_EXPORT_PLAN.json",
        "source_class": "ORIGINAL_TRACE_OR_SOURCE_HEAD_ARTIFACT",
        "json_path": "important_files.src/engine/backtest.py.hits[157].text",
        "matched_pattern": "\"market_shock_gate_enabled\"\\s*:\\s*True",
        "line_text": "        \"market_shock_gate_enabled\": True,",
        "context": []
      },
      "{\"field\": \"market_shock_gate_enabled\", \"source_path\": \"docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F2_E1_BACKTEST_ENTRY_AUDIT.json\", \"source_class\": \"ORIGINAL_TRACE_OR_SOURCE_HEAD_ARTIFACT\", \"json_path\": \"source_report.functions[0].source_head\", \"matched_pattern\": \"market_shock_gate_enabled\\\\s*=\\\\s*bool\\\\(a\\\\.get\\\\(\\\"market_shock_gate_enabled\\\"\", \"line_text\": \"def run_stateful_simulation(\\n    symbols:        list[str],\\n    prices_map:     dict[str, list[float]],\\n    dates_map:      dict[str, list[str]],\\n    spx_prices:     list[float],\\n    spx_dates:      list[str],\\n    ohlc_map:       dict = None,\\n    assumptions:    dict = None,\\n    step:           int  = 1,\\n    min_history:    int  = 120,\\n    market_score_default: float = 60.0,\\n    sim_start_date: str  = None,  # 交易执行起始日（None=从 min_history 后开始）\\n    sim_end_date:   str  = None,  # 交易执行截止日（None=到末尾）\\n    ndx_prices:     list = None,  # NDX 收盘价（Gate v2 Leadership 判断）\\n    ndx_dates:      list = None,\\n    sox_prices:     list = None,  # SOX 收盘价\\n    sox_dates:      list = None,\\n    vix_prices:     list = None,  # VIX 收盘价\\n    vix_dates:      list = None,\\n) -> dict:\\n    \\\"\\\"\\\"\\n    Layer D v1.6: Strict Top3 + RS threshold + MinHold + Relative SPX Stop\\n\\n    修正项（相比 v3）：\\n    1. SPX master calendar — 时间轴以 SPX dates 为准\\n    2. Date-based alignment — 所有股票按日期查找，不用 index 直接对齐\\n    3. skipped_orders_by_reason — 跳过原因分类统计\\n    4. sample_validity 检查 — 样本不足时返回 INSUFFICIENT_SAMPLE\\n    \\\"\\\"\\\"\\n    logger.info(\\\"[Backtest Layer D v1.6] Strict Top3 + RS/MinHold/RelStop Backtest...\\\")\\n\\n    # ── 冻结参数 ─────────────────────────────────────────\\n    a        = assumptions or LAYER_D_ASSUMPTIONS\\n    max_pos  = a[\\\"max_positions\\\"]\\n    buy_pct  = a[\\\"buy_size\\\"]  / max_pos       # Top3: 1/3 per full slot\\n    add_pct  = a[\\\"add_size\\\"]  / max_pos       # Top3: +1/6, only useful after REDUCE\\n    max_pct  = a[\\\"max_single_size\\\"] / max_pos # Top3: max 1/3 per position\\n    one_way  = a[\\\"total_one_way\\\"]             # 0.001\\n    init_cap = float(a.get(\\\"initial_capital\\\", 100_000))\\n    strategy_variant = a.get(\\\"strategy_variant\\\", \\\"top3_entry_rs_minhold_relstop\\\")\\n    e1r_shell_mode = bool(a.get(\\\"e1r_shell_mode\\\", False))\\n    e1r_regime_wiring_enabled = bool(a.get(\\\"e1r_regime_wiring_enabled\\\", False))\\n    e1r_uptrend_execution_enabled = bool(a.get(\\\"e1r_uptrend_execution_enabled\\\", False))\\n    e1r_regime_d...<truncated>"
    ],
    "polluted_examples": [],
    "required": "Assignment/default and usage in _shock_active."
  },
  "market_shock_daily_return": {
    "status": "PASS",
    "clean_evidence_count": 67,
    "primary_source_count": 4,
    "original_trace_or_source_head_count": 63,
    "polluted_evidence_count": 0,
    "best_evidence": [
      {
        "field": "market_shock_daily_return",
        "source_path": "src/engine/backtest.py",
        "source_class": "PRIMARY_SOURCE_CODE",
        "line": 62,
        "matched_pattern": "\"market_shock_daily_return\"\\s*:\\s*-0\\.02",
        "line_text": "    \"market_shock_daily_return\": -0.02,",
        "context": [
          {
            "line": 58,
            "text": "    # the impact of RS threshold, minimum holding period, and relative SPX stop."
          },
          {
            "line": 59,
            "text": "    \"market_gate_enabled\": False,"
          },
          {
            "line": 60,
            "text": "    \"risk_off_below_spx_ma50\": False,"
          },
          {
            "line": 61,
            "text": "    \"market_shock_gate_enabled\": False,"
          },
          {
            "line": 62,
            "text": "    \"market_shock_daily_return\": -0.02,"
          },
          {
            "line": 63,
            "text": ""
          },
          {
            "line": 64,
            "text": "    # Entry / holding / relative-risk controls tested by v1.6 variants."
          },
          {
            "line": 65,
            "text": "    \"entry_rs_min\": 90.0,"
          },
          {
            "line": 66,
            "text": "    \"min_holding_days\": 0,"
          }
        ]
      },
      {
        "field": "market_shock_daily_return",
        "source_path": "src/engine/backtest.py",
        "source_class": "PRIMARY_SOURCE_CODE",
        "line": 897,
        "matched_pattern": "market_shock_daily_return\\s*=\\s*float\\(a\\.get\\(\"market_shock_daily_return\"",
        "line_text": "    market_shock_daily_return = float(a.get(\"market_shock_daily_return\", -0.02))",
        "context": [
          {
            "line": 893,
            "text": "        logger.info(f\"  Entry mode: Strict Top{entry_top_n} (legacy)\")"
          },
          {
            "line": 894,
            "text": "    if ls60_exit_mode not in {\"exit\", \"reduce\"}:"
          },
          {
            "line": 895,
            "text": "        raise ValueError(f\"Invalid ls60_exit_mode={ls60_exit_mode!r}; expected 'exit' or 'reduce'\")"
          },
          {
            "line": 896,
            "text": "    market_shock_gate_enabled = bool(a.get(\"market_shock_gate_enabled\", True))"
          },
          {
            "line": 897,
            "text": "    market_shock_daily_return = float(a.get(\"market_shock_daily_return\", -0.02))"
          },
          {
            "line": 898,
            "text": "    take_profit_enabled = bool(a.get(\"partial_take_profit_enabled\", False))"
          },
          {
            "line": 899,
            "text": "    take_profit_threshold = float(a.get(\"partial_take_profit_threshold\", 0.07))"
          },
          {
            "line": 900,
            "text": "    take_profit_fraction = float(a.get(\"partial_take_profit_fraction\", 0.50))"
          },
          {
            "line": 901,
            "text": "    block_add_after_take_profit = bool(a.get(\"block_add_after_take_profit\", False))"
          }
        ]
      },
      {
        "field": "market_shock_daily_return",
        "source_path": "src/engine/backtest.py",
        "source_class": "PRIMARY_SOURCE_CODE",
        "line": 2529,
        "matched_pattern": "\"market_shock_daily_return\"\\s*:\\s*-0\\.02",
        "line_text": "        \"market_shock_daily_return\": -0.02,",
        "context": [
          {
            "line": 2525,
            "text": "    _gate_v2_no_vix = {"
          },
          {
            "line": 2526,
            "text": "        \"market_gate_enabled\":       True,"
          },
          {
            "line": 2527,
            "text": "        \"risk_off_below_spx_ma50\":   True,"
          },
          {
            "line": 2528,
            "text": "        \"market_shock_gate_enabled\": True,"
          },
          {
            "line": 2529,
            "text": "        \"market_shock_daily_return\": -0.02,"
          },
          {
            "line": 2530,
            "text": "        \"candidate_top_n\":           None,"
          },
          {
            "line": 2531,
            "text": "        \"qualified_entry_enabled\":   False,"
          },
          {
            "line": 2532,
            "text": "        \"fill_only_enabled\":         False,"
          },
          {
            "line": 2533,
            "text": "    }"
          }
        ]
      },
      {
        "field": "market_shock_daily_return",
        "source_path": "src/engine/backtest.py",
        "source_class": "PRIMARY_SOURCE_CODE",
        "line": 2540,
        "matched_pattern": "\"market_shock_daily_return\"\\s*:\\s*-0\\.02",
        "line_text": "        \"market_shock_daily_return\": -0.02,",
        "context": [
          {
            "line": 2536,
            "text": "    _gate_g4 = {"
          },
          {
            "line": 2537,
            "text": "        \"market_gate_enabled\":       True,"
          },
          {
            "line": 2538,
            "text": "        \"risk_off_below_spx_ma50\":   False,"
          },
          {
            "line": 2539,
            "text": "        \"market_shock_gate_enabled\": False,"
          },
          {
            "line": 2540,
            "text": "        \"market_shock_daily_return\": -0.02,"
          },
          {
            "line": 2541,
            "text": "        \"gate_use_slope\":            True,"
          },
          {
            "line": 2542,
            "text": "        \"gate_use_leadership\":       True,"
          },
          {
            "line": 2543,
            "text": "        \"candidate_top_n\":           None,"
          },
          {
            "line": 2544,
            "text": "        \"qualified_entry_enabled\":   False,"
          }
        ]
      },
      "{\"field\": \"market_shock_daily_return\", \"source_path\": \"docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json\", \"source_class\": \"ORIGINAL_TRACE_OR_SOURCE_HEAD_ARTIFACT\", \"line\": 1407, \"matched_pattern\": \"market_shock_daily_return.*-0\\\\.02\", \"line_text\": \"          \\\"source_head\\\": \\\"def run_strategy_variant_comparison(\\\\n    symbols: list[str],\\\\n    prices_map: dict[str, list[float]],\\\\n    dates_map: dict[str, list[str]],\\\\n    spx_prices: list[float],\\\\n    spx_dates: list[str],\\\\n    ndx_prices: list[float] = None,\\\\n    ndx_dates:  list[str]   = None,\\\\n    sox_prices: list[float] = None,\\\\n    sox_dates:  list[str]   = None,\\\\n    vix_prices: list[float] = None,\\\\n    vix_dates:  list[str]   = None,\\\\n) -> dict:\\\\n    \\\\\\\"\\\\\\\"\\\\\\\"\\\\n    Run four diagnostic portfolio variants using Strict Top3, no fixed TP.\\\\n\\\\n    V0_BASE: current Strict Top3 baseline.\\\\n    V1_RS95: raise entry RS threshold from 90 to 95.\\\\n    V2_RS95_MINHOLD5: add minimum 5 trading-day hold for ordinary REDUCE/EXIT.\\\\n    V3_RS95_MINHOLD5_RELSTOP8: add relative SPX underperformance stop.\\\\n\\\\n    Selection policy:\\\\n    1. Prefer PASS over PARTIAL over FAIL.\\\\n    2. Within the same status, prefer higher total return.\\\\n    3. Break ties with higher Profit Factor, higher Sharpe, then lower max drawdown.\\\\n    \\\\\\\"\\\\\\\"\\\\\\\"\\\\n    logger.info(\\\\\\\"[Backtest Layer D v1.6] Strategy Variant Comparison...\\\\\\\")\\\\n\\\\n    base = {\\\\n        **LAYER_D_ASSUMPTIONS,\\\\n        \\\\\\\"market_gate_enabled\\\\\\\": False,\\\\n        \\\\\\\"market_shock_gate_enabled\\\\\\\": False,\\\\n        \\\\\\\"partial_take_profit_enabled\\\\\\\": False,\\\\n        \\\\\\\"block_add_after_take_profit\\\\\\\": False,\\\\n    }\\\\n    # ── Gate v2 No VIX（冻结市场层基准）─────────────────────────\\\\n    _gate_v2_no_vix = {\\\\n        \\\\\\\"market_gate_enabled\\\\\\\":       True,\\\\n        \\\\\\\"risk_off_below_spx_ma50\\\\\\\":   True,\\\\n        \\\\\\\"market_shock_gate_enabled\\\\\\\": True,\\\\n        \\\\\\\"market_shock_daily_retur\", \"context\": [{\"line\": 1403, \"text\": \"            \\\"MA_CONFLICT\\\",\"}, {\"line\": 1404, \"text\": \"            \\\"E1R_REGIME_AWARE_V0_2\\\",\"}, {\"line\": 1405, \"text\": \"            \\\"E1R_REGIME_AWARE_V0_1\\\"\"}, {\"line\": 1406, \"text\": \"          ],\"}, {\"line\": 1407, \"text\": \"          \\\"source_head\\\": \\\"def run_strategy_variant_comparison(\\\\n    symbols: list[str],\\\\n    prices_map: dict[str, list[float]],\\\\n    dates_map: dict[str, list[st...<truncated>",
      "{\"field\": \"market_shock_daily_return\", \"source_path\": \"docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json\", \"source_class\": \"ORIGINAL_TRACE_OR_SOURCE_HEAD_ARTIFACT\", \"json_path\": \"source_file_reports.src/engine/backtest.py.functions[3].source_head\", \"matched_pattern\": \"\\\"market_shock_daily_return\\\"\\\\s*:\\\\s*-0\\\\.02\", \"line_text\": \"def run_strategy_variant_comparison(\\n    symbols: list[str],\\n    prices_map: dict[str, list[float]],\\n    dates_map: dict[str, list[str]],\\n    spx_prices: list[float],\\n    spx_dates: list[str],\\n    ndx_prices: list[float] = None,\\n    ndx_dates:  list[str]   = None,\\n    sox_prices: list[float] = None,\\n    sox_dates:  list[str]   = None,\\n    vix_prices: list[float] = None,\\n    vix_dates:  list[str]   = None,\\n) -> dict:\\n    \\\"\\\"\\\"\\n    Run four diagnostic portfolio variants using Strict Top3, no fixed TP.\\n\\n    V0_BASE: current Strict Top3 baseline.\\n    V1_RS95: raise entry RS threshold from 90 to 95.\\n    V2_RS95_MINHOLD5: add minimum 5 trading-day hold for ordinary REDUCE/EXIT.\\n    V3_RS95_MINHOLD5_RELSTOP8: add relative SPX underperformance stop.\\n\\n    Selection policy:\\n    1. Prefer PASS over PARTIAL over FAIL.\\n    2. Within the same status, prefer higher total return.\\n    3. Break ties with higher Profit Factor, higher Sharpe, then lower max drawdown.\\n    \\\"\\\"\\\"\\n    logger.info(\\\"[Backtest Layer D v1.6] Strategy Variant Comparison...\\\")\\n\\n    base = {\\n        **LAYER_D_ASSUMPTIONS,\\n        \\\"market_gate_enabled\\\": False,\\n        \\\"market_shock_gate_enabled\\\": False,\\n        \\\"partial_take_profit_enabled\\\": False,\\n        \\\"block_add_after_take_profit\\\": False,\\n    }\\n    # ── Gate v2 No VIX（冻结市场层基准）─────────────────────────\\n    _gate_v2_no_vix = {\\n        \\\"market_gate_enabled\\\":       True,\\n        \\\"risk_off_below_spx_ma50\\\":   True,\\n        \\\"market_shock_gate_enabled\\\": True,\\n        \\\"market_shock_daily_return\\\": -0.02,\\n        \\\"candidate_top_n\\\":           None,\\n        \\\"qualified_entry_enabled\\\":   False,\\n        \\\"fill_only_enabled\\\":         False,\\n    }\\n\\n    # ── E2 实验配置（Gate 固定 G4，只改退出层）────────────────\\n    _gate_g4 = {\\n        \\\"market_gate_enabled\\\":       True,\\n        \\\"risk_off_below_spx_ma50\\\":   False,\\n        \\\"market_shock_gate_enabled\\\": False,\\n        \\\"market_shock_daily_return\\\": -0.02,\\n        \\\"gate_use_slope\\\":            True,\\n   ...<truncated>",
      {
        "field": "market_shock_daily_return",
        "source_path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0_E1_E1R_CORE_CONTRACT_AUDIT.json",
        "source_class": "ORIGINAL_TRACE_OR_SOURCE_HEAD_ARTIFACT",
        "line": 2701,
        "matched_pattern": "market_shock_daily_return.*-0\\.02",
        "line_text": "            \"text\": \"    market_shock_daily_return = float(a.get(\\\"market_shock_daily_return\\\", -0.02))\"",
        "context": [
          {
            "line": 2697,
            "text": "            \"text\": \"    market_shock_gate_enabled = bool(a.get(\\\"market_shock_gate_enabled\\\", True))\""
          },
          {
            "line": 2698,
            "text": "          },"
          },
          {
            "line": 2699,
            "text": "          {"
          },
          {
            "line": 2700,
            "text": "            \"line\": 897,"
          },
          {
            "line": 2701,
            "text": "            \"text\": \"    market_shock_daily_return = float(a.get(\\\"market_shock_daily_return\\\", -0.02))\""
          },
          {
            "line": 2702,
            "text": "          }"
          },
          {
            "line": 2703,
            "text": "        ]"
          },
          {
            "line": 2704,
            "text": "      },"
          },
          {
            "line": 2705,
            "text": "      {"
          }
        ]
      },
      "{\"field\": \"market_shock_daily_return\", \"source_path\": \"docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0_E1_E1R_CORE_CONTRACT_AUDIT.json\", \"source_class\": \"ORIGINAL_TRACE_OR_SOURCE_HEAD_ARTIFACT\", \"line\": 10648, \"matched_pattern\": \"market_shock_daily_return.*-0\\\\.02\", \"line_text\": \"        \\\"source\\\": \\\"def run_stateful_simulation(\\\\n    symbols:        list[str],\\\\n    prices_map:     dict[str, list[float]],\\\\n    dates_map:      dict[str, list[str]],\\\\n    spx_prices:     list[float],\\\\n    spx_dates:      list[str],\\\\n    ohlc_map:       dict = None,\\\\n    assumptions:    dict = None,\\\\n    step:           int  = 1,\\\\n    min_history:    int  = 120,\\\\n    market_score_default: float = 60.0,\\\\n    sim_start_date: str  = None,  # 交易执行起始日（None=从 min_history 后开始）\\\\n    sim_end_date:   str  = None,  # 交易执行截止日（None=到末尾）\\\\n    ndx_prices:     list = None,  # NDX 收盘价（Gate v2 Leadership 判断）\\\\n    ndx_dates:      list = None,\\\\n    sox_prices:     list = None,  # SOX 收盘价\\\\n    sox_dates:      list = None,\\\\n    vix_prices:     list = None,  # VIX 收盘价\\\\n    vix_dates:      list = None,\\\\n) -> dict:\\\\n    \\\\\\\"\\\\\\\"\\\\\\\"\\\\n    Layer D v1.6: Strict Top3 + RS threshold + MinHold + Relative SPX Stop\\\\n\\\\n    修正项（相比 v3）：\\\\n    1. SPX master calendar — 时间轴以 SPX dates 为准\\\\n    2. Date-based alignment — 所有股票按日期查找，不用 index 直接对齐\\\\n    3. skipped_orders_by_reason — 跳过原因分类统计\\\\n    4. sample_validity 检查 — 样本不足时返回 INSUFFICIENT_SAMPLE\\\\n    \\\\\\\"\\\\\\\"\\\\\\\"\\\\n    logger.info(\\\\\\\"[Backtest Layer D v1.6] Strict Top3 + RS/MinHold/RelStop Backtest...\\\\\\\")\\\\n\\\\n    # ── 冻结参数 ─────────────────────────────────────────\\\\n    a        = assumptions or LAYER_D_ASSUMPTIONS\\\\n    max_pos  = a[\\\\\\\"max_positions\\\\\\\"]\\\\n    buy_pct  = a[\\\\\\\"buy_size\\\\\\\"]  / max_pos       # Top3: 1/3 per full slot\\\\n    add_pct  = a[\\\\\\\"add_size\\\\\\\"]  / max_pos       # Top3: +1/6, only useful after REDUCE\\\\n    max_pct  = a[\\\\\\\"max_single_size\\\\\\\"] / max_pos # Top3: max 1/3 per posi\", \"context\": [{\"line\": 10644, \"text\": \"      \\\"run_stateful_simulation\\\": {\"}, {\"line\": 10645, \"text\": \"        \\\"path\\\": \\\"src/engine/backtest.py\\\",\"}, {\"line\": 10646, \"text\": \"        \\\"line\\\": 763,\"}, {\"line\": 10647, \"text\": \"        \\\"end_line\\\": 2486,\"}, {\"line\": 10648, \"text\": \"        \\\"source\\\": \\\"def run_stateful_simulation(\\\\n    symbols:        list[str],\\\\n    prices_map:     dict[str, list[float]],\\\\n    dates_map:      dict[str, lis...<truncated>",
      "{\"field\": \"market_shock_daily_return\", \"source_path\": \"docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0_E1_E1R_CORE_CONTRACT_AUDIT.json\", \"source_class\": \"ORIGINAL_TRACE_OR_SOURCE_HEAD_ARTIFACT\", \"line\": 10654, \"matched_pattern\": \"market_shock_daily_return.*-0\\\\.02\", \"line_text\": \"        \\\"source\\\": \\\"def run_strategy_variant_comparison(\\\\n    symbols: list[str],\\\\n    prices_map: dict[str, list[float]],\\\\n    dates_map: dict[str, list[str]],\\\\n    spx_prices: list[float],\\\\n    spx_dates: list[str],\\\\n    ndx_prices: list[float] = None,\\\\n    ndx_dates:  list[str]   = None,\\\\n    sox_prices: list[float] = None,\\\\n    sox_dates:  list[str]   = None,\\\\n    vix_prices: list[float] = None,\\\\n    vix_dates:  list[str]   = None,\\\\n) -> dict:\\\\n    \\\\\\\"\\\\\\\"\\\\\\\"\\\\n    Run four diagnostic portfolio variants using Strict Top3, no fixed TP.\\\\n\\\\n    V0_BASE: current Strict Top3 baseline.\\\\n    V1_RS95: raise entry RS threshold from 90 to 95.\\\\n    V2_RS95_MINHOLD5: add minimum 5 trading-day hold for ordinary REDUCE/EXIT.\\\\n    V3_RS95_MINHOLD5_RELSTOP8: add relative SPX underperformance stop.\\\\n\\\\n    Selection policy:\\\\n    1. Prefer PASS over PARTIAL over FAIL.\\\\n    2. Within the same status, prefer higher total return.\\\\n    3. Break ties with higher Profit Factor, higher Sharpe, then lower max drawdown.\\\\n    \\\\\\\"\\\\\\\"\\\\\\\"\\\\n    logger.info(\\\\\\\"[Backtest Layer D v1.6] Strategy Variant Comparison...\\\\\\\")\\\\n\\\\n    base = {\\\\n        **LAYER_D_ASSUMPTIONS,\\\\n        \\\\\\\"market_gate_enabled\\\\\\\": False,\\\\n        \\\\\\\"market_shock_gate_enabled\\\\\\\": False,\\\\n        \\\\\\\"partial_take_profit_enabled\\\\\\\": False,\\\\n        \\\\\\\"block_add_after_take_profit\\\\\\\": False,\\\\n    }\\\\n    # ── Gate v2 No VIX（冻结市场层基准）─────────────────────────\\\\n    _gate_v2_no_vix = {\\\\n        \\\\\\\"market_gate_enabled\\\\\\\":       True,\\\\n        \\\\\\\"risk_off_below_spx_ma50\\\\\\\":   True,\\\\n        \\\\\\\"market_shock_gate_enabled\\\\\\\": True,\\\\n        \\\\\\\"market_shock_daily_return\\\\\\\": -0\", \"context\": [{\"line\": 10650, \"text\": \"      \\\"run_strategy_variant_comparison\\\": {\"}, {\"line\": 10651, \"text\": \"        \\\"path\\\": \\\"src/engine/backtest.py\\\",\"}, {\"line\": 10652, \"text\": \"        \\\"line\\\": 2489,\"}, {\"line\": 10653, \"text\": \"        \\\"end_line\\\": 2895,\"}, {\"line\": 10654, \"text\": \"        \\\"source\\\": \\\"def run_strategy_variant_comparison(\\\\n    symbols: list[str],\\\\n    prices_map: dict[str, list[float]],\\\\n    dat...<truncated>",
      {
        "field": "market_shock_daily_return",
        "source_path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0_E1_E1R_CORE_CONTRACT_AUDIT.json",
        "source_class": "ORIGINAL_TRACE_OR_SOURCE_HEAD_ARTIFACT",
        "json_path": "source_hits.src/engine/backtest.py[13].context",
        "matched_pattern": "market_shock_daily_return.*-0\\.02",
        "line_text": "[{\"line\": 893, \"text\": \"        logger.info(f\\\"  Entry mode: Strict Top{entry_top_n} (legacy)\\\")\"}, {\"line\": 894, \"text\": \"    if ls60_exit_mode not in {\\\"exit\\\", \\\"reduce\\\"}:\"}, {\"line\": 895, \"text\": \"        raise ValueError(f\\\"Invalid ls60_exit_mode={ls60_exit_mode!r}; expected 'exit' or 'reduce'\\\")\"}, {\"line\": 896, \"text\": \"    market_shock_gate_enabled = bool(a.get(\\\"market_shock_gate_enabled\\\", True))\"}, {\"line\": 897, \"text\": \"    market_shock_daily_return = float(a.get(\\\"market_shock_daily_return\\\", -0.02))\"}]",
        "context": []
      },
      {
        "field": "market_shock_daily_return",
        "source_path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0_E1_E1R_CORE_CONTRACT_AUDIT.json",
        "source_class": "ORIGINAL_TRACE_OR_SOURCE_HEAD_ARTIFACT",
        "json_path": "source_hits.src/engine/backtest.py[13].context[4].text",
        "matched_pattern": "market_shock_daily_return\\s*=\\s*float\\(a\\.get\\(\"market_shock_daily_return\"",
        "line_text": "    market_shock_daily_return = float(a.get(\"market_shock_daily_return\", -0.02))",
        "context": []
      },
      "{\"field\": \"market_shock_daily_return\", \"source_path\": \"docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0_E1_E1R_CORE_CONTRACT_AUDIT.json\", \"source_class\": \"ORIGINAL_TRACE_OR_SOURCE_HEAD_ARTIFACT\", \"json_path\": \"function_sources.src/engine/backtest.py.run_stateful_simulation.source\", \"matched_pattern\": \"market_shock_daily_return\\\\s*=\\\\s*float\\\\(a\\\\.get\\\\(\\\"market_shock_daily_return\\\"\", \"line_text\": \"def run_stateful_simulation(\\n    symbols:        list[str],\\n    prices_map:     dict[str, list[float]],\\n    dates_map:      dict[str, list[str]],\\n    spx_prices:     list[float],\\n    spx_dates:      list[str],\\n    ohlc_map:       dict = None,\\n    assumptions:    dict = None,\\n    step:           int  = 1,\\n    min_history:    int  = 120,\\n    market_score_default: float = 60.0,\\n    sim_start_date: str  = None,  # 交易执行起始日（None=从 min_history 后开始）\\n    sim_end_date:   str  = None,  # 交易执行截止日（None=到末尾）\\n    ndx_prices:     list = None,  # NDX 收盘价（Gate v2 Leadership 判断）\\n    ndx_dates:      list = None,\\n    sox_prices:     list = None,  # SOX 收盘价\\n    sox_dates:      list = None,\\n    vix_prices:     list = None,  # VIX 收盘价\\n    vix_dates:      list = None,\\n) -> dict:\\n    \\\"\\\"\\\"\\n    Layer D v1.6: Strict Top3 + RS threshold + MinHold + Relative SPX Stop\\n\\n    修正项（相比 v3）：\\n    1. SPX master calendar — 时间轴以 SPX dates 为准\\n    2. Date-based alignment — 所有股票按日期查找，不用 index 直接对齐\\n    3. skipped_orders_by_reason — 跳过原因分类统计\\n    4. sample_validity 检查 — 样本不足时返回 INSUFFICIENT_SAMPLE\\n    \\\"\\\"\\\"\\n    logger.info(\\\"[Backtest Layer D v1.6] Strict Top3 + RS/MinHold/RelStop Backtest...\\\")\\n\\n    # ── 冻结参数 ─────────────────────────────────────────\\n    a        = assumptions or LAYER_D_ASSUMPTIONS\\n    max_pos  = a[\\\"max_positions\\\"]\\n    buy_pct  = a[\\\"buy_size\\\"]  / max_pos       # Top3: 1/3 per full slot\\n    add_pct  = a[\\\"add_size\\\"]  / max_pos       # Top3: +1/6, only useful after REDUCE\\n    max_pct  = a[\\\"max_single_size\\\"] / max_pos # Top3: max 1/3 per position\\n    one_way  = a[\\\"total_one_way\\\"]             # 0.001\\n    init_cap = float(a.get(\\\"initial_capital\\\", 100_000))\\n    strategy_variant = a.get(\\\"strategy_variant\\\", \\\"top3_entry_rs_minhold_relstop\\\")\\n    e1r_shell_mode = bool(a.get(\\\"e1r_shell_mode\\\", False))\\n    e1r_regime_wiring_enabled = bool(a.get(\\\"e1r_regime_wiring_enabled\\\", False))\\n    e1r_uptrend_execution_enabled = bool(a.get(\\\"e1r_uptrend_executio...<truncated>"
    ],
    "polluted_examples": [],
    "required": "Assignment/default value -0.02 and usage in _shock_active."
  },
  "market_entry_gate_or_equivalent": {
    "status": "PASS",
    "clean_evidence_count": 156,
    "primary_source_count": 13,
    "original_trace_or_source_head_count": 143,
    "polluted_evidence_count": 0,
    "best_evidence": [
      {
        "field": "market_entry_gate_or_equivalent",
        "source_path": "src/engine/backtest.py",
        "source_class": "PRIMARY_SOURCE_CODE",
        "line": 1396,
        "matched_pattern": "entry_capacity",
        "line_text": "            entry_capacity   = max_pos",
        "context": [
          {
            "line": 1392,
            "text": "        # ── Gate v2：三档市场状态 ────────────────────────────────"
          },
          {
            "line": 1393,
            "text": "        if not market_gate_enabled:"
          },
          {
            "line": 1394,
            "text": "            # Gate 关闭：完全跳过，不执行任何 Gate v2 计算"
          },
          {
            "line": 1395,
            "text": "            market_state     = \"FULL_ON\""
          },
          {
            "line": 1396,
            "text": "            entry_capacity   = max_pos"
          },
          {
            "line": 1397,
            "text": "            market_risk_off  = False"
          },
          {
            "line": 1398,
            "text": "            market_shock     = False"
          },
          {
            "line": 1399,
            "text": "            market_entry_allowed = True"
          },
          {
            "line": 1400,
            "text": "            market_gate_days[\"entry_allowed\"] += 1"
          }
        ]
      },
      {
        "field": "market_entry_gate_or_equivalent",
        "source_path": "src/engine/backtest.py",
        "source_class": "PRIMARY_SOURCE_CODE",
        "line": 1399,
        "matched_pattern": "market_entry_allowed\\s*=",
        "line_text": "            market_entry_allowed = True",
        "context": [
          {
            "line": 1395,
            "text": "            market_state     = \"FULL_ON\""
          },
          {
            "line": 1396,
            "text": "            entry_capacity   = max_pos"
          },
          {
            "line": 1397,
            "text": "            market_risk_off  = False"
          },
          {
            "line": 1398,
            "text": "            market_shock     = False"
          },
          {
            "line": 1399,
            "text": "            market_entry_allowed = True"
          },
          {
            "line": 1400,
            "text": "            market_gate_days[\"entry_allowed\"] += 1"
          },
          {
            "line": 1401,
            "text": "        else:"
          },
          {
            "line": 1402,
            "text": "            # ── MA50 slope（10日变化率，使用完整历史索引，无 warm-up 问题）"
          },
          {
            "line": 1403,
            "text": "            if t >= 59:  # t>=49（MA50）+ 10（slope 回溯）"
          }
        ]
      },
      {
        "field": "market_entry_gate_or_equivalent",
        "source_path": "src/engine/backtest.py",
        "source_class": "PRIMARY_SOURCE_CODE",
        "line": 1470,
        "matched_pattern": "entry_capacity",
        "line_text": "                entry_capacity = 0",
        "context": [
          {
            "line": 1466,
            "text": "                or (gate_use_slope and spx_ma50_slope < 0)"
          },
          {
            "line": 1467,
            "text": "            )"
          },
          {
            "line": 1468,
            "text": "            if _cash_mode:"
          },
          {
            "line": 1469,
            "text": "                market_state   = \"CASH_MODE\""
          },
          {
            "line": 1470,
            "text": "                entry_capacity = 0"
          },
          {
            "line": 1471,
            "text": "            elif ("
          },
          {
            "line": 1472,
            "text": "                _spx_above"
          },
          {
            "line": 1473,
            "text": "                and _slope_ok"
          },
          {
            "line": 1474,
            "text": "                and _leadership_strong"
          }
        ]
      },
      {
        "field": "market_entry_gate_or_equivalent",
        "source_path": "src/engine/backtest.py",
        "source_class": "PRIMARY_SOURCE_CODE",
        "line": 1478,
        "matched_pattern": "entry_capacity",
        "line_text": "                entry_capacity = max_pos",
        "context": [
          {
            "line": 1474,
            "text": "                and _leadership_strong"
          },
          {
            "line": 1475,
            "text": "                and not _shock_active"
          },
          {
            "line": 1476,
            "text": "            ):"
          },
          {
            "line": 1477,
            "text": "                market_state   = \"FULL_ON\""
          },
          {
            "line": 1478,
            "text": "                entry_capacity = max_pos"
          },
          {
            "line": 1479,
            "text": "            else:"
          },
          {
            "line": 1480,
            "text": "                market_state   = \"CAUTIOUS_ON\""
          },
          {
            "line": 1481,
            "text": "                entry_capacity = min(max_pos, 2)"
          },
          {
            "line": 1482,
            "text": ""
          }
        ]
      },
      {
        "field": "market_entry_gate_or_equivalent",
        "source_path": "src/engine/backtest.py",
        "source_class": "PRIMARY_SOURCE_CODE",
        "line": 1481,
        "matched_pattern": "entry_capacity",
        "line_text": "                entry_capacity = min(max_pos, 2)",
        "context": [
          {
            "line": 1477,
            "text": "                market_state   = \"FULL_ON\""
          },
          {
            "line": 1478,
            "text": "                entry_capacity = max_pos"
          },
          {
            "line": 1479,
            "text": "            else:"
          },
          {
            "line": 1480,
            "text": "                market_state   = \"CAUTIOUS_ON\""
          },
          {
            "line": 1481,
            "text": "                entry_capacity = min(max_pos, 2)"
          },
          {
            "line": 1482,
            "text": ""
          },
          {
            "line": 1483,
            "text": "            market_risk_off  = (market_state == \"CASH_MODE\") and not _shock_active"
          },
          {
            "line": 1484,
            "text": "            market_shock     = _shock_active"
          },
          {
            "line": 1485,
            "text": "            market_entry_allowed = entry_capacity > 0"
          }
        ]
      },
      {
        "field": "market_entry_gate_or_equivalent",
        "source_path": "src/engine/backtest.py",
        "source_class": "PRIMARY_SOURCE_CODE",
        "line": 1485,
        "matched_pattern": "market_entry_allowed\\s*=",
        "line_text": "            market_entry_allowed = entry_capacity > 0",
        "context": [
          {
            "line": 1481,
            "text": "                entry_capacity = min(max_pos, 2)"
          },
          {
            "line": 1482,
            "text": ""
          },
          {
            "line": 1483,
            "text": "            market_risk_off  = (market_state == \"CASH_MODE\") and not _shock_active"
          },
          {
            "line": 1484,
            "text": "            market_shock     = _shock_active"
          },
          {
            "line": 1485,
            "text": "            market_entry_allowed = entry_capacity > 0"
          },
          {
            "line": 1486,
            "text": ""
          },
          {
            "line": 1487,
            "text": "            if market_risk_off:"
          },
          {
            "line": 1488,
            "text": "                market_gate_days[\"risk_off\"] += 1"
          },
          {
            "line": 1489,
            "text": "            if market_shock:"
          }
        ]
      },
      {
        "field": "market_entry_gate_or_equivalent",
        "source_path": "src/engine/backtest.py",
        "source_class": "PRIMARY_SOURCE_CODE",
        "line": 1510,
        "matched_pattern": "_gate_state\\s*=",
        "line_text": "        _gate_state = (",
        "context": [
          {
            "line": 1506,
            "text": "        _drawdown_pct = ("
          },
          {
            "line": 1507,
            "text": "            (daily_equity_peak - total_equity) / daily_equity_peak * 100"
          },
          {
            "line": 1508,
            "text": "            if daily_equity_peak and daily_equity_peak > 0 else 0.0"
          },
          {
            "line": 1509,
            "text": "        )"
          },
          {
            "line": 1510,
            "text": "        _gate_state = ("
          },
          {
            "line": 1511,
            "text": "            \"ALLOW\" if market_entry_allowed else"
          },
          {
            "line": 1512,
            "text": "            \"SHOCK\" if market_shock else \"RISK_OFF\""
          },
          {
            "line": 1513,
            "text": "        )"
          },
          {
            "line": 1514,
            "text": ""
          }
        ]
      },
      {
        "field": "market_entry_gate_or_equivalent",
        "source_path": "src/engine/backtest.py",
        "source_class": "PRIMARY_SOURCE_CODE",
        "line": 1718,
        "matched_pattern": "entry_capacity",
        "line_text": "                if len(holdings) < min(max_pos, entry_capacity):",
        "context": [
          {
            "line": 1714,
            "text": "                    v,"
          },
          {
            "line": 1715,
            "text": "                ))"
          },
          {
            "line": 1716,
            "text": "            e1r_buy_candidates.sort()"
          },
          {
            "line": 1717,
            "text": "            if e1r_buy_candidates and market_entry_allowed:"
          },
          {
            "line": 1718,
            "text": "                if len(holdings) < min(max_pos, entry_capacity):"
          },
          {
            "line": 1719,
            "text": "                    _, _, _, _, _, _sym, _sig = e1r_buy_candidates[0]"
          },
          {
            "line": 1720,
            "text": "                    _etype = _sig.get(\"e1r_entry_type\")"
          },
          {
            "line": 1721,
            "text": "                    e1r_selected_buy = {"
          },
          {
            "line": 1722,
            "text": "                        \"sym\": _sym,"
          }
        ]
      },
      {
        "field": "market_entry_gate_or_equivalent",
        "source_path": "src/engine/backtest.py",
        "source_class": "PRIMARY_SOURCE_CODE",
        "line": 1816,
        "matched_pattern": "entry_capacity",
        "line_text": "                    if fill_only_enabled and len(holdings) >= entry_capacity:",
        "context": [
          {
            "line": 1812,
            "text": "                        action = \"ADD\""
          },
          {
            "line": 1813,
            "text": "                elif sym in top_entry_symbols:"
          },
          {
            "line": 1814,
            "text": "                    # sym 在 Qualified Pool 候选里"
          },
          {
            "line": 1815,
            "text": "                    # Fill-Only 检查：如果开启，只在有空仓位时才允许买入"
          },
          {
            "line": 1816,
            "text": "                    if fill_only_enabled and len(holdings) >= entry_capacity:"
          },
          {
            "line": 1817,
            "text": "                        skip_reasons[\"fill_only_no_empty_slot\"] += 1"
          },
          {
            "line": 1818,
            "text": "                        continue"
          },
          {
            "line": 1819,
            "text": "                    # → 允许开仓（Gate 启用时才在 STEP 3 检查容量）"
          },
          {
            "line": 1820,
            "text": "                    if market_gate_enabled and len(holdings) >= entry_capacity:"
          }
        ]
      },
      {
        "field": "market_entry_gate_or_equivalent",
        "source_path": "src/engine/backtest.py",
        "source_class": "PRIMARY_SOURCE_CODE",
        "line": 1820,
        "matched_pattern": "entry_capacity",
        "line_text": "                    if market_gate_enabled and len(holdings) >= entry_capacity:",
        "context": [
          {
            "line": 1816,
            "text": "                    if fill_only_enabled and len(holdings) >= entry_capacity:"
          },
          {
            "line": 1817,
            "text": "                        skip_reasons[\"fill_only_no_empty_slot\"] += 1"
          },
          {
            "line": 1818,
            "text": "                        continue"
          },
          {
            "line": 1819,
            "text": "                    # → 允许开仓（Gate 启用时才在 STEP 3 检查容量）"
          },
          {
            "line": 1820,
            "text": "                    if market_gate_enabled and len(holdings) >= entry_capacity:"
          },
          {
            "line": 1821,
            "text": "                        skip_reasons[\"gate_capacity_block\"] = skip_reasons.get(\"gate_capacity_block\", 0) + 1"
          },
          {
            "line": 1822,
            "text": "                        continue"
          },
          {
            "line": 1823,
            "text": "                    if not market_entry_allowed:"
          },
          {
            "line": 1824,
            "text": "                        reason = \"market_shock_block\" if market_shock else \"market_risk_off_block\""
          }
        ]
      },
      {
        "field": "market_entry_gate_or_equivalent",
        "source_path": "src/engine/backtest.py",
        "source_class": "PRIMARY_SOURCE_CODE",
        "line": 1872,
        "matched_pattern": "entry_capacity",
        "line_text": "                    if market_gate_enabled and len(holdings) >= entry_capacity:",
        "context": [
          {
            "line": 1868,
            "text": "                        skip_reasons[\"not_in_entry_top_n\"] += 1"
          },
          {
            "line": 1869,
            "text": "                        continue"
          },
          {
            "line": 1870,
            "text": "                    # STEP 3 容量检查：只在 Gate 启用时才在信号生成层拦截"
          },
          {
            "line": 1871,
            "text": "                    # Gate OFF 时依赖 STEP 1 执行层的 max_positions_reached 检查"
          },
          {
            "line": 1872,
            "text": "                    if market_gate_enabled and len(holdings) >= entry_capacity:"
          },
          {
            "line": 1873,
            "text": "                        skip_reasons[\"gate_capacity_block\"] = skip_reasons.get(\"gate_capacity_block\", 0) + 1"
          },
          {
            "line": 1874,
            "text": "                        continue"
          },
          {
            "line": 1875,
            "text": "                    if not market_entry_allowed:"
          },
          {
            "line": 1876,
            "text": "                        reason = \"market_shock_block\" if market_shock else \"market_risk_off_block\""
          }
        ]
      },
      {
        "field": "market_entry_gate_or_equivalent",
        "source_path": "src/engine/backtest.py",
        "source_class": "PRIMARY_SOURCE_CODE",
        "line": 2412,
        "matched_pattern": "blocked_actions",
        "line_text": "            \"blocked_actions\": [\"BUY\", \"ADD\"],",
        "context": [
          {
            "line": 2408,
            "text": "            \"market_shock_rule\": ("
          },
          {
            "line": 2409,
            "text": "                f\"SPX daily return <= {market_shock_daily_return*100:.1f}%\""
          },
          {
            "line": 2410,
            "text": "                if market_shock_gate_enabled else \"disabled\""
          },
          {
            "line": 2411,
            "text": "            ),"
          },
          {
            "line": 2412,
            "text": "            \"blocked_actions\": [\"BUY\", \"ADD\"],"
          },
          {
            "line": 2413,
            "text": "            \"unaffected_actions\": [\"HOLD\", \"REDUCE\", \"EXIT\"],"
          },
          {
            "line": 2414,
            "text": "            \"days\": market_gate_days,"
          },
          {
            "line": 2415,
            "text": "        },"
          },
          {
            "line": 2416,
            "text": "        # 样本有效性（完整字段）"
          }
        ]
      }
    ],
    "polluted_examples": [],
    "required": "Source evidence for gate output or equivalent BUY/ADD blocking and HOLD/REDUCE/EXIT unaffected behavior."
  },
  "e1r_v0_2_core_call_chain": {
    "status": "PASS",
    "clean_evidence_count": 1292,
    "primary_source_count": 18,
    "original_trace_or_source_head_count": 1254,
    "polluted_evidence_count": 0,
    "best_evidence": [
      {
        "field": "e1r_v0_2_core_call_chain",
        "source_path": "src/engine/backtest.py",
        "source_class": "PRIMARY_SOURCE_CODE",
        "line": 763,
        "matched_pattern": "run_stateful_simulation",
        "line_text": "def run_stateful_simulation(",
        "context": [
          {
            "line": 759,
            "text": "# ══════════════════════════════════════════════════════════════════"
          },
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
          },
          {
            "line": 767,
            "text": "    spx_prices:     list[float],"
          }
        ]
      },
      {
        "field": "e1r_v0_2_core_call_chain",
        "source_path": "src/engine/backtest.py",
        "source_class": "PRIMARY_SOURCE_CODE",
        "line": 2646,
        "matched_pattern": "run_stateful_simulation",
        "line_text": "            _result = run_stateful_simulation(",
        "context": [
          {
            "line": 2642,
            "text": "            # E1/E2：Gate G4 固定使用 NDX/SOX（leadership），不传 VIX"
          },
          {
            "line": 2643,
            "text": "            _use_ndx = ndx_prices or []"
          },
          {
            "line": 2644,
            "text": "            _use_sox = sox_prices or []"
          },
          {
            "line": 2645,
            "text": "            _use_vix = []  # Gate v2.1 不使用 VIX"
          },
          {
            "line": 2646,
            "text": "            _result = run_stateful_simulation("
          },
          {
            "line": 2647,
            "text": "                symbols=symbols,"
          },
          {
            "line": 2648,
            "text": "                prices_map=prices_map,"
          },
          {
            "line": 2649,
            "text": "                dates_map=dates_map,"
          },
          {
            "line": 2650,
            "text": "                spx_prices=spx_prices,"
          }
        ]
      },
      {
        "field": "e1r_v0_2_core_call_chain",
        "source_path": "src/engine/backtest.py",
        "source_class": "PRIMARY_SOURCE_CODE",
        "line": 2695,
        "matched_pattern": "run_stateful_simulation",
        "line_text": "    # - Do not modify run_stateful_simulation().",
        "context": [
          {
            "line": 2691,
            "text": ""
          },
          {
            "line": 2692,
            "text": "    # ── E1-R v0.2 formal sidecar sleeve composition ────────────────"
          },
          {
            "line": 2693,
            "text": "    #"
          },
          {
            "line": 2694,
            "text": "    # Design principle:"
          },
          {
            "line": 2695,
            "text": "    # - Do not modify run_stateful_simulation()."
          },
          {
            "line": 2696,
            "text": "    # - Do not modify E1R_REGIME_AWARE_V0_1."
          },
          {
            "line": 2697,
            "text": "    # - Compose the validated SIDEWAYS:MA_CONFLICT Top10 25% sleeve"
          },
          {
            "line": 2698,
            "text": "    #   with the existing E1R v0.1 core daily returns."
          },
          {
            "line": 2699,
            "text": "    #"
          }
        ]
      },
      {
        "field": "e1r_v0_2_core_call_chain",
        "source_path": "src/engine/backtest.py",
        "source_class": "PRIMARY_SOURCE_CODE",
        "line": 2708,
        "matched_pattern": "compose_e1r_v0_2_variant",
        "line_text": "        from src.engine.e1r_composer import compose_e1r_v0_2_variant",
        "context": [
          {
            "line": 2704,
            "text": "        from src.engine.e1r_sidecar_sleeve import ("
          },
          {
            "line": 2705,
            "text": "            E1RSidecarConfig,"
          },
          {
            "line": 2706,
            "text": "            build_e1r_sidecar_sleeve,"
          },
          {
            "line": 2707,
            "text": "        )"
          },
          {
            "line": 2708,
            "text": "        from src.engine.e1r_composer import compose_e1r_v0_2_variant"
          },
          {
            "line": 2709,
            "text": ""
          },
          {
            "line": 2710,
            "text": "        _core_e1r = variant_results.get(\"E1R_REGIME_AWARE_V0_1\")"
          },
          {
            "line": 2711,
            "text": "        _core_records = (_core_e1r or {}).get(\"daily_equity_records\", []) if _core_e1r else []"
          },
          {
            "line": 2712,
            "text": ""
          }
        ]
      },
      {
        "field": "e1r_v0_2_core_call_chain",
        "source_path": "src/engine/backtest.py",
        "source_class": "PRIMARY_SOURCE_CODE",
        "line": 2710,
        "matched_pattern": "_core_e1r",
        "line_text": "        _core_e1r = variant_results.get(\"E1R_REGIME_AWARE_V0_1\")",
        "context": [
          {
            "line": 2706,
            "text": "            build_e1r_sidecar_sleeve,"
          },
          {
            "line": 2707,
            "text": "        )"
          },
          {
            "line": 2708,
            "text": "        from src.engine.e1r_composer import compose_e1r_v0_2_variant"
          },
          {
            "line": 2709,
            "text": ""
          },
          {
            "line": 2710,
            "text": "        _core_e1r = variant_results.get(\"E1R_REGIME_AWARE_V0_1\")"
          },
          {
            "line": 2711,
            "text": "        _core_records = (_core_e1r or {}).get(\"daily_equity_records\", []) if _core_e1r else []"
          },
          {
            "line": 2712,
            "text": ""
          },
          {
            "line": 2713,
            "text": "        _stock_dir = Path(\"data/research/e1_5y/raw/stocks\")"
          },
          {
            "line": 2714,
            "text": "        _spx_path = Path(\"data/research/e1_5y/raw/indices/SPX.json\")"
          }
        ]
      },
      {
        "field": "e1r_v0_2_core_call_chain",
        "source_path": "src/engine/backtest.py",
        "source_class": "PRIMARY_SOURCE_CODE",
        "line": 2711,
        "matched_pattern": "_core_e1r",
        "line_text": "        _core_records = (_core_e1r or {}).get(\"daily_equity_records\", []) if _core_e1r else []",
        "context": [
          {
            "line": 2707,
            "text": "        )"
          },
          {
            "line": 2708,
            "text": "        from src.engine.e1r_composer import compose_e1r_v0_2_variant"
          },
          {
            "line": 2709,
            "text": ""
          },
          {
            "line": 2710,
            "text": "        _core_e1r = variant_results.get(\"E1R_REGIME_AWARE_V0_1\")"
          },
          {
            "line": 2711,
            "text": "        _core_records = (_core_e1r or {}).get(\"daily_equity_records\", []) if _core_e1r else []"
          },
          {
            "line": 2712,
            "text": ""
          },
          {
            "line": 2713,
            "text": "        _stock_dir = Path(\"data/research/e1_5y/raw/stocks\")"
          },
          {
            "line": 2714,
            "text": "        _spx_path = Path(\"data/research/e1_5y/raw/indices/SPX.json\")"
          },
          {
            "line": 2715,
            "text": "        _regime_path = Path(\"data/research/e1_5y/regimes/spx_regime_daily.json\")"
          }
        ]
      },
      {
        "field": "e1r_v0_2_core_call_chain",
        "source_path": "src/engine/backtest.py",
        "source_class": "PRIMARY_SOURCE_CODE",
        "line": 2717,
        "matched_pattern": "_core_e1r",
        "line_text": "        if _core_e1r and _core_records and _stock_dir.exists() and _spx_path.exists() and _regime_path.exists():",
        "context": [
          {
            "line": 2713,
            "text": "        _stock_dir = Path(\"data/research/e1_5y/raw/stocks\")"
          },
          {
            "line": 2714,
            "text": "        _spx_path = Path(\"data/research/e1_5y/raw/indices/SPX.json\")"
          },
          {
            "line": 2715,
            "text": "        _regime_path = Path(\"data/research/e1_5y/regimes/spx_regime_daily.json\")"
          },
          {
            "line": 2716,
            "text": ""
          },
          {
            "line": 2717,
            "text": "        if _core_e1r and _core_records and _stock_dir.exists() and _spx_path.exists() and _regime_path.exists():"
          },
          {
            "line": 2718,
            "text": "            _sidecar_cfg = E1RSidecarConfig("
          },
          {
            "line": 2719,
            "text": "                start_date=_core_records[0][\"date\"],"
          },
          {
            "line": 2720,
            "text": "                end_date=_core_records[-1][\"date\"],"
          },
          {
            "line": 2721,
            "text": "                allowed_subclasses=(\"MA_CONFLICT\",),"
          }
        ]
      },
      {
        "field": "e1r_v0_2_core_call_chain",
        "source_path": "src/engine/backtest.py",
        "source_class": "PRIMARY_SOURCE_CODE",
        "line": 2737,
        "matched_pattern": "compose_e1r_v0_2_variant",
        "line_text": "            variant_results[\"E1R_REGIME_AWARE_V0_2\"] = compose_e1r_v0_2_variant(",
        "context": [
          {
            "line": 2733,
            "text": "                regime_path=_regime_path,"
          },
          {
            "line": 2734,
            "text": "                config=_sidecar_cfg,"
          },
          {
            "line": 2735,
            "text": "            )"
          },
          {
            "line": 2736,
            "text": ""
          },
          {
            "line": 2737,
            "text": "            variant_results[\"E1R_REGIME_AWARE_V0_2\"] = compose_e1r_v0_2_variant("
          },
          {
            "line": 2738,
            "text": "                core_variant_result=_core_e1r,"
          },
          {
            "line": 2739,
            "text": "                sidecar_result=_sidecar_result,"
          },
          {
            "line": 2740,
            "text": "                initial_equity=float(base.get(\"initial_capital\", 100000)),"
          },
          {
            "line": 2741,
            "text": "            )"
          }
        ]
      },
      {
        "field": "e1r_v0_2_core_call_chain",
        "source_path": "src/engine/backtest.py",
        "source_class": "PRIMARY_SOURCE_CODE",
        "line": 2738,
        "matched_pattern": "core_variant_result",
        "line_text": "                core_variant_result=_core_e1r,",
        "context": [
          {
            "line": 2734,
            "text": "                config=_sidecar_cfg,"
          },
          {
            "line": 2735,
            "text": "            )"
          },
          {
            "line": 2736,
            "text": ""
          },
          {
            "line": 2737,
            "text": "            variant_results[\"E1R_REGIME_AWARE_V0_2\"] = compose_e1r_v0_2_variant("
          },
          {
            "line": 2738,
            "text": "                core_variant_result=_core_e1r,"
          },
          {
            "line": 2739,
            "text": "                sidecar_result=_sidecar_result,"
          },
          {
            "line": 2740,
            "text": "                initial_equity=float(base.get(\"initial_capital\", 100000)),"
          },
          {
            "line": 2741,
            "text": "            )"
          },
          {
            "line": 2742,
            "text": ""
          }
        ]
      },
      {
        "field": "e1r_v0_2_core_call_chain",
        "source_path": "src/engine/e1r_composer.py",
        "source_class": "PRIMARY_SOURCE_CODE",
        "line": 9,
        "matched_pattern": "E1R_REGIME_AWARE_V0_2",
        "line_text": "- E1R_REGIME_AWARE_V0_2 formal combined daily equity records",
        "context": [
          {
            "line": 5,
            "text": "- E1R_REGIME_AWARE_V0_1 core daily equity records"
          },
          {
            "line": 6,
            "text": "- E1R sidecar sleeve daily return records"
          },
          {
            "line": 7,
            "text": ""
          },
          {
            "line": 8,
            "text": "into:"
          },
          {
            "line": 9,
            "text": "- E1R_REGIME_AWARE_V0_2 formal combined daily equity records"
          },
          {
            "line": 10,
            "text": ""
          },
          {
            "line": 11,
            "text": "Alignment rule"
          },
          {
            "line": 12,
            "text": "--------------"
          },
          {
            "line": 13,
            "text": "Core daily equity record date means:"
          }
        ]
      },
      {
        "field": "e1r_v0_2_core_call_chain",
        "source_path": "src/engine/e1r_composer.py",
        "source_class": "PRIMARY_SOURCE_CODE",
        "line": 283,
        "matched_pattern": "compose_e1r_v0_2_variant",
        "line_text": "def compose_e1r_v0_2_variant(",
        "context": [
          {
            "line": 279,
            "text": "        },"
          },
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
          },
          {
            "line": 287,
            "text": ") -> dict[str, Any]:"
          }
        ]
      },
      {
        "field": "e1r_v0_2_core_call_chain",
        "source_path": "src/engine/e1r_composer.py",
        "source_class": "PRIMARY_SOURCE_CODE",
        "line": 284,
        "matched_pattern": "core_variant_result",
        "line_text": "    core_variant_result: dict[str, Any],",
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
          },
          {
            "line": 287,
            "text": ") -> dict[str, Any]:"
          },
          {
            "line": 288,
            "text": "    core_records = core_variant_result.get(\"daily_equity_records\", [])"
          }
        ]
      }
    ],
    "polluted_examples": [],
    "required": "run_stateful_simulation -> core_variant_result/_core_e1r -> compose_e1r_v0_2_variant."
  },
  "e1r_v0_2_sidecar_call_chain": {
    "status": "PASS",
    "clean_evidence_count": 2056,
    "primary_source_count": 40,
    "original_trace_or_source_head_count": 1971,
    "polluted_evidence_count": 0,
    "best_evidence": [
      {
        "field": "e1r_v0_2_sidecar_call_chain",
        "source_path": "src/engine/backtest.py",
        "source_class": "PRIMARY_SOURCE_CODE",
        "line": 2697,
        "matched_pattern": "MA_CONFLICT",
        "line_text": "    # - Compose the validated SIDEWAYS:MA_CONFLICT Top10 25% sleeve",
        "context": [
          {
            "line": 2693,
            "text": "    #"
          },
          {
            "line": 2694,
            "text": "    # Design principle:"
          },
          {
            "line": 2695,
            "text": "    # - Do not modify run_stateful_simulation()."
          },
          {
            "line": 2696,
            "text": "    # - Do not modify E1R_REGIME_AWARE_V0_1."
          },
          {
            "line": 2697,
            "text": "    # - Compose the validated SIDEWAYS:MA_CONFLICT Top10 25% sleeve"
          },
          {
            "line": 2698,
            "text": "    #   with the existing E1R v0.1 core daily returns."
          },
          {
            "line": 2699,
            "text": "    #"
          },
          {
            "line": 2700,
            "text": "    # This keeps the formal engine semantics aligned with the validated"
          },
          {
            "line": 2701,
            "text": "    # research S4 sidecar instead of approximating it inside the Top3"
          }
        ]
      },
      {
        "field": "e1r_v0_2_sidecar_call_chain",
        "source_path": "src/engine/backtest.py",
        "source_class": "PRIMARY_SOURCE_CODE",
        "line": 2706,
        "matched_pattern": "build_e1r_sidecar_sleeve",
        "line_text": "            build_e1r_sidecar_sleeve,",
        "context": [
          {
            "line": 2702,
            "text": "    # stateful order loop."
          },
          {
            "line": 2703,
            "text": "    try:"
          },
          {
            "line": 2704,
            "text": "        from src.engine.e1r_sidecar_sleeve import ("
          },
          {
            "line": 2705,
            "text": "            E1RSidecarConfig,"
          },
          {
            "line": 2706,
            "text": "            build_e1r_sidecar_sleeve,"
          },
          {
            "line": 2707,
            "text": "        )"
          },
          {
            "line": 2708,
            "text": "        from src.engine.e1r_composer import compose_e1r_v0_2_variant"
          },
          {
            "line": 2709,
            "text": ""
          },
          {
            "line": 2710,
            "text": "        _core_e1r = variant_results.get(\"E1R_REGIME_AWARE_V0_1\")"
          }
        ]
      },
      {
        "field": "e1r_v0_2_sidecar_call_chain",
        "source_path": "src/engine/backtest.py",
        "source_class": "PRIMARY_SOURCE_CODE",
        "line": 2708,
        "matched_pattern": "compose_e1r_v0_2_variant",
        "line_text": "        from src.engine.e1r_composer import compose_e1r_v0_2_variant",
        "context": [
          {
            "line": 2704,
            "text": "        from src.engine.e1r_sidecar_sleeve import ("
          },
          {
            "line": 2705,
            "text": "            E1RSidecarConfig,"
          },
          {
            "line": 2706,
            "text": "            build_e1r_sidecar_sleeve,"
          },
          {
            "line": 2707,
            "text": "        )"
          },
          {
            "line": 2708,
            "text": "        from src.engine.e1r_composer import compose_e1r_v0_2_variant"
          },
          {
            "line": 2709,
            "text": ""
          },
          {
            "line": 2710,
            "text": "        _core_e1r = variant_results.get(\"E1R_REGIME_AWARE_V0_1\")"
          },
          {
            "line": 2711,
            "text": "        _core_records = (_core_e1r or {}).get(\"daily_equity_records\", []) if _core_e1r else []"
          },
          {
            "line": 2712,
            "text": ""
          }
        ]
      },
      {
        "field": "e1r_v0_2_sidecar_call_chain",
        "source_path": "src/engine/backtest.py",
        "source_class": "PRIMARY_SOURCE_CODE",
        "line": 2721,
        "matched_pattern": "MA_CONFLICT",
        "line_text": "                allowed_subclasses=(\"MA_CONFLICT\",),",
        "context": [
          {
            "line": 2717,
            "text": "        if _core_e1r and _core_records and _stock_dir.exists() and _spx_path.exists() and _regime_path.exists():"
          },
          {
            "line": 2718,
            "text": "            _sidecar_cfg = E1RSidecarConfig("
          },
          {
            "line": 2719,
            "text": "                start_date=_core_records[0][\"date\"],"
          },
          {
            "line": 2720,
            "text": "                end_date=_core_records[-1][\"date\"],"
          },
          {
            "line": 2721,
            "text": "                allowed_subclasses=(\"MA_CONFLICT\",),"
          },
          {
            "line": 2722,
            "text": "                top_n=10,"
          },
          {
            "line": 2723,
            "text": "                gross_exposure=0.25,"
          },
          {
            "line": 2724,
            "text": "                min_history_days=200,"
          },
          {
            "line": 2725,
            "text": "                min_price=5.0,"
          }
        ]
      },
      {
        "field": "e1r_v0_2_sidecar_call_chain",
        "source_path": "src/engine/backtest.py",
        "source_class": "PRIMARY_SOURCE_CODE",
        "line": 2723,
        "matched_pattern": "gross_exposure",
        "line_text": "                gross_exposure=0.25,",
        "context": [
          {
            "line": 2719,
            "text": "                start_date=_core_records[0][\"date\"],"
          },
          {
            "line": 2720,
            "text": "                end_date=_core_records[-1][\"date\"],"
          },
          {
            "line": 2721,
            "text": "                allowed_subclasses=(\"MA_CONFLICT\",),"
          },
          {
            "line": 2722,
            "text": "                top_n=10,"
          },
          {
            "line": 2723,
            "text": "                gross_exposure=0.25,"
          },
          {
            "line": 2724,
            "text": "                min_history_days=200,"
          },
          {
            "line": 2725,
            "text": "                min_price=5.0,"
          },
          {
            "line": 2726,
            "text": "                initial_equity=float(base.get(\"initial_capital\", 100000)),"
          },
          {
            "line": 2727,
            "text": "                excluded_symbols=(\"VIXY\",),"
          }
        ]
      },
      {
        "field": "e1r_v0_2_sidecar_call_chain",
        "source_path": "src/engine/backtest.py",
        "source_class": "PRIMARY_SOURCE_CODE",
        "line": 2730,
        "matched_pattern": "build_e1r_sidecar_sleeve",
        "line_text": "            _sidecar_result = build_e1r_sidecar_sleeve(",
        "context": [
          {
            "line": 2726,
            "text": "                initial_equity=float(base.get(\"initial_capital\", 100000)),"
          },
          {
            "line": 2727,
            "text": "                excluded_symbols=(\"VIXY\",),"
          },
          {
            "line": 2728,
            "text": "            )"
          },
          {
            "line": 2729,
            "text": ""
          },
          {
            "line": 2730,
            "text": "            _sidecar_result = build_e1r_sidecar_sleeve("
          },
          {
            "line": 2731,
            "text": "                stock_dir=_stock_dir,"
          },
          {
            "line": 2732,
            "text": "                spx_path=_spx_path,"
          },
          {
            "line": 2733,
            "text": "                regime_path=_regime_path,"
          },
          {
            "line": 2734,
            "text": "                config=_sidecar_cfg,"
          }
        ]
      },
      {
        "field": "e1r_v0_2_sidecar_call_chain",
        "source_path": "src/engine/backtest.py",
        "source_class": "PRIMARY_SOURCE_CODE",
        "line": 2737,
        "matched_pattern": "compose_e1r_v0_2_variant",
        "line_text": "            variant_results[\"E1R_REGIME_AWARE_V0_2\"] = compose_e1r_v0_2_variant(",
        "context": [
          {
            "line": 2733,
            "text": "                regime_path=_regime_path,"
          },
          {
            "line": 2734,
            "text": "                config=_sidecar_cfg,"
          },
          {
            "line": 2735,
            "text": "            )"
          },
          {
            "line": 2736,
            "text": ""
          },
          {
            "line": 2737,
            "text": "            variant_results[\"E1R_REGIME_AWARE_V0_2\"] = compose_e1r_v0_2_variant("
          },
          {
            "line": 2738,
            "text": "                core_variant_result=_core_e1r,"
          },
          {
            "line": 2739,
            "text": "                sidecar_result=_sidecar_result,"
          },
          {
            "line": 2740,
            "text": "                initial_equity=float(base.get(\"initial_capital\", 100000)),"
          },
          {
            "line": 2741,
            "text": "            )"
          }
        ]
      },
      {
        "field": "e1r_v0_2_sidecar_call_chain",
        "source_path": "src/engine/backtest.py",
        "source_class": "PRIMARY_SOURCE_CODE",
        "line": 2739,
        "matched_pattern": "sidecar_result",
        "line_text": "                sidecar_result=_sidecar_result,",
        "context": [
          {
            "line": 2735,
            "text": "            )"
          },
          {
            "line": 2736,
            "text": ""
          },
          {
            "line": 2737,
            "text": "            variant_results[\"E1R_REGIME_AWARE_V0_2\"] = compose_e1r_v0_2_variant("
          },
          {
            "line": 2738,
            "text": "                core_variant_result=_core_e1r,"
          },
          {
            "line": 2739,
            "text": "                sidecar_result=_sidecar_result,"
          },
          {
            "line": 2740,
            "text": "                initial_equity=float(base.get(\"initial_capital\", 100000)),"
          },
          {
            "line": 2741,
            "text": "            )"
          },
          {
            "line": 2742,
            "text": ""
          },
          {
            "line": 2743,
            "text": "            _sidecar_summary = _sidecar_result.get(\"summary\", {}) or {}"
          }
        ]
      },
      {
        "field": "e1r_v0_2_sidecar_call_chain",
        "source_path": "src/engine/backtest.py",
        "source_class": "PRIMARY_SOURCE_CODE",
        "line": 2743,
        "matched_pattern": "sidecar_result",
        "line_text": "            _sidecar_summary = _sidecar_result.get(\"summary\", {}) or {}",
        "context": [
          {
            "line": 2739,
            "text": "                sidecar_result=_sidecar_result,"
          },
          {
            "line": 2740,
            "text": "                initial_equity=float(base.get(\"initial_capital\", 100000)),"
          },
          {
            "line": 2741,
            "text": "            )"
          },
          {
            "line": 2742,
            "text": ""
          },
          {
            "line": 2743,
            "text": "            _sidecar_summary = _sidecar_result.get(\"summary\", {}) or {}"
          },
          {
            "line": 2744,
            "text": "            logger.info("
          },
          {
            "line": 2745,
            "text": "                \"  E1-R v0.2 formal sidecar sleeve composed: \""
          },
          {
            "line": 2746,
            "text": "                f\"active_days={_sidecar_summary.get('active_days')} \""
          },
          {
            "line": 2747,
            "text": "                f\"return={_sidecar_summary.get('full_period_strategy_return_pct'):.2f}%\""
          }
        ]
      },
      {
        "field": "e1r_v0_2_sidecar_call_chain",
        "source_path": "src/engine/e1r_composer.py",
        "source_class": "PRIMARY_SOURCE_CODE",
        "line": 164,
        "matched_pattern": "gross_exposure",
        "line_text": "            \"sidecar_gross_exposure\": sidecar.get(\"gross_exposure\"),",
        "context": [
          {
            "line": 160,
            "text": "            \"regime\": sidecar.get(\"regime\"),"
          },
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
          },
          {
            "line": 168,
            "text": "    return aligned"
          }
        ]
      },
      {
        "field": "e1r_v0_2_sidecar_call_chain",
        "source_path": "src/engine/e1r_composer.py",
        "source_class": "PRIMARY_SOURCE_CODE",
        "line": 208,
        "matched_pattern": "gross_exposure",
        "line_text": "            \"sidecar_gross_exposure\": row.get(\"sidecar_gross_exposure\"),",
        "context": [
          {
            "line": 204,
            "text": "            \"spx_regime\": row.get(\"regime\"),"
          },
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
          },
          {
            "line": 212,
            "text": ""
          }
        ]
      },
      {
        "field": "e1r_v0_2_sidecar_call_chain",
        "source_path": "src/engine/e1r_composer.py",
        "source_class": "PRIMARY_SOURCE_CODE",
        "line": 283,
        "matched_pattern": "compose_e1r_v0_2_variant",
        "line_text": "def compose_e1r_v0_2_variant(",
        "context": [
          {
            "line": 279,
            "text": "        },"
          },
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
          },
          {
            "line": 287,
            "text": ") -> dict[str, Any]:"
          }
        ]
      }
    ],
    "polluted_examples": [],
    "required": "build_e1r_sidecar_sleeve -> sidecar_result -> compose_e1r_v0_2_variant, MA_CONFLICT 135-row sleeve."
  }
}
```

## Field Status Counts
```json
{
  "PASS": 7
}
```

## Blocking Fields
```json
[]
```

## Validations
```json
{
  "market_param_source_line_trace_complete": true,
  "rca2_loaded": true,
  "target_artifact_exists": true,
  "generator_trace_exists": true,
  "primary_source_files_inspected": true,
  "trace_candidate_paths_extracted": true,
  "evidence_matrix_built": true,
  "required_fields_count": 7,
  "source_line_all_fields_pass": true,
  "blocking_fields_count": 0,
  "strategy_logic_changed": false,
  "audit_only": true,
  "formula_not_patched": true,
  "backtest_engine_run": false,
  "short_window_existing_engine_run": false,
  "full_5y_backtest_run": false,
  "forward_runner_run": false,
  "candidate_generation_extracted": false,
  "buy_add_reduce_exit_extracted": false,
  "official_result_generated": false,
  "dashboard_changed": false,
  "strategy_files_unchanged": true
}
```

## Decision
```json
{
  "k2_r9d_market_param_source_line_trace_passed": true,
  "market_state_115_replication_ready": true,
  "formula_patch_allowed_now": false,
  "candidate_extraction_allowed_now": false,
  "implementation_may_resume": false,
  "blocking_fields": [],
  "next_required_stage_if_ready": "4C-2C-4E-ENGINE-K2-R10-MARKET_GATE_STANDALONE_REPLICATION_PROPOSAL",
  "next_required_stage_if_not_ready": "4C-2C-4E-ENGINE-K2-R9E-MARKET_PARAM_GAP_CLOSURE_PLAN",
  "conclusion": "K2_R9D_PASS_SOURCE_LINE_EVIDENCE_READY_FOR_R10_PROPOSAL",
  "recommended_next_action": "Proceed to R10 only if every evidence matrix field is PASS. If any field is PARTIAL/FAIL, prepare a gap-closure plan instead of implementing."
}
```
