# E1R 4C-2C-4E-ENGINE-K2-R10 — Market Gate Standalone Replication Proposal

Generated At: `2026-07-11T03:40:44.027485+00:00`

## Purpose
Convert R7/R8/R9D evidence into a standalone market gate replication design proposal without implementation.

## Scope
R10 is proposal-only. It does not create `src/e1r_engine/market_gate.py`, does not patch strategy logic, and does not run any backtest.

## Proposal
```json
{
  "proposal_id": "E1R_MARKET_GATE_STANDALONE_REPLICATION_PROPOSAL_V1",
  "proposal_scope": "Design only. No implementation in R10.",
  "source_evidence_inputs": {
    "r7_short_window_source_equivalence": "docs/research/E1R_4C2C4E_ENGINE_K2_R7_MARKET_STATE_SOURCE_EQUIVALENCE_TRACE.json",
    "r8_short_window_parameter_audit": "docs/research/E1R_4C2C4E_ENGINE_K2_R8_MARKET_STATE_PARAMETER_AUDIT.json",
    "r9d_full_artifact_source_line_evidence": "docs/research/E1R_4C2C4E_ENGINE_K2_R9D_MARKET_PARAM_SOURCE_LINE_TRACE.json",
    "rca2_stop_review": "docs/research/E1R_4C2C4E_ENGINE_K2_RCA2_MARKET_PARAM_EVIDENCE_CHAIN_REVIEW.json"
  },
  "r9d_evidence_summary": {
    "market_gate_enabled": {
      "status": "PASS",
      "clean_evidence_count": 29,
      "primary_source_count": 3,
      "original_trace_or_source_head_count": 26,
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
        "{\"field\": \"market_gate_enabled\", \"source_path\": \"docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json\", \"source_class\": \"ORIGINAL_TRACE_OR_SOURCE_HEAD_ARTIFACT\", \"json_path\": \"source_file_reports.src/engine/backtest.py.functions[3].source_head\", \"matched_pattern\": \"\\\"market_gate_enabled\\\"\\\\s*:\\\\s*True\", \"line_text\": \"def run_strategy_variant_comparison(\\n    symbols: list[str],\\n    prices_map: dict[str, list[float]],\\n    dates_map: dict[str, list[str]],\\n    spx_prices: list[float],\\n    spx_dates: list[str],\\n    ndx_prices: list[float] = None,\\n    ndx_dates:  list[str]   = None,\\n    sox_prices: list[float] = None,\\n    sox_dates:  list[str]   = None,\\n    vix_prices: list[float] = None,\\n    vix_dates:  list[str]   = None,\\n) -> dict:\\n    \\\"\\\"\\\"\\n    Run four diagnostic portfolio variants using Strict Top3, no fixed TP.\\n\\n    V0_BASE: current Strict Top3 baseline.\\n    V1_RS95: raise entry RS threshold from 90 to 95.\\n    V2_RS95_MINHOLD5: add minimum 5 trading-day hold for ordinary REDUCE/EXIT.\\n    V3_RS95_MINHOLD5_RELSTOP8: add relative SPX underperformance stop.\\n\\n    Selection policy:\\n    1. Prefer PASS over PARTIAL over FAIL.\\n    2. Within the same status, prefer higher total return.\\n    3. Break ties with higher Profit Factor, higher Sharpe, then lower max drawdown.\\n    \\\"\\\"\\\"\\n    logger.info(\\\"[Backtest Layer D v1.6] Strategy Variant Comparison...\\\")\\n\\n    base = {\\n        **LAYER_D_ASSUMPTIONS,\\n        \\\"market_gate_enabled\\\": False,\\n        \\\"market_shock_gate_enabled\\\": False,\\n        \\\"partial_take_profit_enabled\\\": False,\\n        \\\"block_add_after_take_profit\\\": False,\\n    }\\n    # ── Gate v2 No VIX（冻结市场层基准）─────────────────────────\\n    _gate_v2_no_vix = {\\n        \\\"market_gate_enabled\\\":       True,\\n        \\\"risk_off_below_spx_ma50\\\":   True,\\n        \\\"market_shock_gate_enabled\\\": True,\\n        \\\"market_shock_daily_return\\\": -0.02,\\n        \\\"candidate_top_n\\\":           None,\\n        \\\"qualified_entry_enabled\\\":   False,\\n        \\\"fill_only_enabled\\\":         False,\\n    }\\n\\n    # ── E2 实验配置（Gate 固定 G4，只改退出层）────────────────\\n    _gate_g4 = {\\n        \\\"market_gate_enabled\\\":       True,\\n     ...<truncated>"
      ]
    },
    "risk_off_below_spx_ma50": {
      "status": "PASS",
      "clean_evidence_count": 20,
      "primary_source_count": 2,
      "original_trace_or_source_head_count": 18,
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
        "{\"field\": \"risk_off_below_spx_ma50\", \"source_path\": \"docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json\", \"source_class\": \"ORIGINAL_TRACE_OR_SOURCE_HEAD_ARTIFACT\", \"json_path\": \"source_file_reports.src/engine/backtest.py.functions[3].source_head\", \"matched_pattern\": \"\\\"risk_off_below_spx_ma50\\\"\\\\s*:\\\\s*True\", \"line_text\": \"def run_strategy_variant_comparison(\\n    symbols: list[str],\\n    prices_map: dict[str, list[float]],\\n    dates_map: dict[str, list[str]],\\n    spx_prices: list[float],\\n    spx_dates: list[str],\\n    ndx_prices: list[float] = None,\\n    ndx_dates:  list[str]   = None,\\n    sox_prices: list[float] = None,\\n    sox_dates:  list[str]   = None,\\n    vix_prices: list[float] = None,\\n    vix_dates:  list[str]   = None,\\n) -> dict:\\n    \\\"\\\"\\\"\\n    Run four diagnostic portfolio variants using Strict Top3, no fixed TP.\\n\\n    V0_BASE: current Strict Top3 baseline.\\n    V1_RS95: raise entry RS threshold from 90 to 95.\\n    V2_RS95_MINHOLD5: add minimum 5 trading-day hold for ordinary REDUCE/EXIT.\\n    V3_RS95_MINHOLD5_RELSTOP8: add relative SPX underperformance stop.\\n\\n    Selection policy:\\n    1. Prefer PASS over PARTIAL over FAIL.\\n    2. Within the same status, prefer higher total return.\\n    3. Break ties with higher Profit Factor, higher Sharpe, then lower max drawdown.\\n    \\\"\\\"\\\"\\n    logger.info(\\\"[Backtest Layer D v1.6] Strategy Variant Comparison...\\\")\\n\\n    base = {\\n        **LAYER_D_ASSUMPTIONS,\\n        \\\"market_gate_enabled\\\": False,\\n        \\\"market_shock_gate_enabled\\\": False,\\n        \\\"partial_take_profit_enabled\\\": False,\\n        \\\"block_add_after_take_profit\\\": False,\\n    }\\n    # ── Gate v2 No VIX（冻结市场层基准）─────────────────────────\\n    _gate_v2_no_vix = {\\n        \\\"market_gate_enabled\\\":       True,\\n        \\\"risk_off_below_spx_ma50\\\":   True,\\n        \\\"market_shock_gate_enabled\\\": True,\\n        \\\"market_shock_daily_return\\\": -0.02,\\n        \\\"candidate_top_n\\\":           None,\\n        \\\"qualified_entry_enabled\\\":   False,\\n        \\\"fill_only_enabled\\\":         False,\\n    }\\n\\n    # ── E2 实验配置（Gate 固定 G4，只改退出层）────────────────\\n    _gate_g4 = {\\n        \\\"market_gate_enabled\\\":       True...<truncated>",
        {
          "field": "risk_off_below_spx_ma50",
          "source_path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0_E1_E1R_CORE_CONTRACT_AUDIT.json",
          "source_class": "ORIGINAL_TRACE_OR_SOURCE_HEAD_ARTIFACT",
          "json_path": "source_hits.src/engine/backtest.py[11].context[1].text",
          "matched_pattern": "risk_off_below_spx_ma50\\s*=\\s*bool\\(a\\.get\\(\"risk_off_below_spx_ma50\"",
          "line_text": "    risk_off_below_spx_ma50 = bool(a.get(\"risk_off_below_spx_ma50\", True))",
          "context": []
        }
      ]
    },
    "market_shock_gate_enabled": {
      "status": "PASS",
      "clean_evidence_count": 22,
      "primary_source_count": 2,
      "original_trace_or_source_head_count": 20,
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
        "{\"field\": \"market_shock_gate_enabled\", \"source_path\": \"docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json\", \"source_class\": \"ORIGINAL_TRACE_OR_SOURCE_HEAD_ARTIFACT\", \"json_path\": \"source_file_reports.src/engine/backtest.py.functions[3].source_head\", \"matched_pattern\": \"\\\"market_shock_gate_enabled\\\"\\\\s*:\\\\s*True\", \"line_text\": \"def run_strategy_variant_comparison(\\n    symbols: list[str],\\n    prices_map: dict[str, list[float]],\\n    dates_map: dict[str, list[str]],\\n    spx_prices: list[float],\\n    spx_dates: list[str],\\n    ndx_prices: list[float] = None,\\n    ndx_dates:  list[str]   = None,\\n    sox_prices: list[float] = None,\\n    sox_dates:  list[str]   = None,\\n    vix_prices: list[float] = None,\\n    vix_dates:  list[str]   = None,\\n) -> dict:\\n    \\\"\\\"\\\"\\n    Run four diagnostic portfolio variants using Strict Top3, no fixed TP.\\n\\n    V0_BASE: current Strict Top3 baseline.\\n    V1_RS95: raise entry RS threshold from 90 to 95.\\n    V2_RS95_MINHOLD5: add minimum 5 trading-day hold for ordinary REDUCE/EXIT.\\n    V3_RS95_MINHOLD5_RELSTOP8: add relative SPX underperformance stop.\\n\\n    Selection policy:\\n    1. Prefer PASS over PARTIAL over FAIL.\\n    2. Within the same status, prefer higher total return.\\n    3. Break ties with higher Profit Factor, higher Sharpe, then lower max drawdown.\\n    \\\"\\\"\\\"\\n    logger.info(\\\"[Backtest Layer D v1.6] Strategy Variant Comparison...\\\")\\n\\n    base = {\\n        **LAYER_D_ASSUMPTIONS,\\n        \\\"market_gate_enabled\\\": False,\\n        \\\"market_shock_gate_enabled\\\": False,\\n        \\\"partial_take_profit_enabled\\\": False,\\n        \\\"block_add_after_take_profit\\\": False,\\n    }\\n    # ── Gate v2 No VIX（冻结市场层基准）─────────────────────────\\n    _gate_v2_no_vix = {\\n        \\\"market_gate_enabled\\\":       True,\\n        \\\"risk_off_below_spx_ma50\\\":   True,\\n        \\\"market_shock_gate_enabled\\\": True,\\n        \\\"market_shock_daily_return\\\": -0.02,\\n        \\\"candidate_top_n\\\":           None,\\n        \\\"qualified_entry_enabled\\\":   False,\\n        \\\"fill_only_enabled\\\":         False,\\n    }\\n\\n    # ── E2 实验配置（Gate 固定 G4，只改退出层）────────────────\\n    _gate_g4 = {\\n        \\\"market_gate_enabled\\\":       ...<truncated>",
        {
          "field": "market_shock_gate_enabled",
          "source_path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0_E1_E1R_CORE_CONTRACT_AUDIT.json",
          "source_class": "ORIGINAL_TRACE_OR_SOURCE_HEAD_ARTIFACT",
          "json_path": "source_hits.src/engine/backtest.py[12].context[4].text",
          "matched_pattern": "market_shock_gate_enabled\\s*=\\s*bool\\(a\\.get\\(\"market_shock_gate_enabled\"",
          "line_text": "    market_shock_gate_enabled = bool(a.get(\"market_shock_gate_enabled\", True))",
          "context": []
        }
      ]
    },
    "market_shock_daily_return": {
      "status": "PASS",
      "clean_evidence_count": 67,
      "primary_source_count": 4,
      "original_trace_or_source_head_count": 63,
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
        }
      ]
    },
    "market_entry_gate_or_equivalent": {
      "status": "PASS",
      "clean_evidence_count": 156,
      "primary_source_count": 13,
      "original_trace_or_source_head_count": 143,
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
        }
      ]
    },
    "e1r_v0_2_core_call_chain": {
      "status": "PASS",
      "clean_evidence_count": 1292,
      "primary_source_count": 18,
      "original_trace_or_source_head_count": 1254,
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
        }
      ]
    },
    "e1r_v0_2_sidecar_call_chain": {
      "status": "PASS",
      "clean_evidence_count": 2056,
      "primary_source_count": 40,
      "original_trace_or_source_head_count": 1971,
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
        }
      ]
    }
  },
  "replication_target": {
    "target_component": "market gate / market state chain used by legacy E1R v0.2 core",
    "do_not_replicate_as": [
      "same-day SPX close < SPX MA50 direct formula",
      "rounded daily_equity_records display-only formula",
      "audit-report evidence-count formula"
    ],
    "replicate_as": [
      "legacy local-variable chain",
      "market_state + _shock_active + entry_capacity",
      "market_entry_allowed + market_shock + market_risk_off",
      "_gate_state export identity"
    ]
  },
  "proposed_module": {
    "file": "src/e1r_engine/market_gate.py",
    "classes": [
      {
        "name": "MarketGateConfig",
        "purpose": "Hold source-proven market gate settings.",
        "fields": {
          "variant": "D3_RISK_OFF_PLUS_SHOCK_GATE",
          "market_gate_enabled": true,
          "risk_off_below_spx_ma50": true,
          "market_shock_gate_enabled": true,
          "market_shock_daily_return": -0.02
        },
        "source": "R8 + R9D"
      },
      {
        "name": "MarketGateInputs",
        "purpose": "Carry precomputed legacy-equivalent upstream values for one trading day.",
        "fields": {
          "date": "YYYY-MM-DD",
          "spx_close": "float | None",
          "spx_ma50": "float | None",
          "spx_day_return": "float | None",
          "market_state": "FULL_ON | CAUTIOUS_ON | CASH_MODE | UNKNOWN",
          "entry_capacity": "int",
          "existing_positions_count": "int"
        },
        "boundary": "Inputs are data/state facts; this object must not rank candidates or decide BUY/ADD/REDUCE/EXIT."
      },
      {
        "name": "MarketGateDecision",
        "purpose": "Return the exact gate-related local outputs needed by later strategy branches.",
        "fields": {
          "market_shock": "bool",
          "market_risk_off": "bool",
          "market_entry_allowed": "bool",
          "entry_capacity": "int",
          "gate_state": "ALLOW | SHOCK | RISK_OFF",
          "blocked_actions": [
            "BUY",
            "ADD"
          ],
          "unaffected_actions": [
            "HOLD",
            "REDUCE",
            "EXIT"
          ],
          "trace": "dict"
        }
      },
      {
        "name": "MarketGateEvaluator",
        "purpose": "Pure deterministic evaluator for market gate state. No order generation.",
        "methods": [
          "evaluate(config: MarketGateConfig, inputs: MarketGateInputs) -> MarketGateDecision"
        ]
      }
    ]
  },
  "source_equivalent_logic_contract": {
    "market_shock": "_shock_active = market_shock_gate_enabled and spx_day_return <= market_shock_daily_return",
    "market_risk_off": "market_risk_off = (market_state == 'CASH_MODE') and not market_shock",
    "market_entry_allowed": "market_entry_allowed = entry_capacity > 0",
    "gate_state": "_gate_state = 'ALLOW' if market_entry_allowed else 'SHOCK' if market_shock else 'RISK_OFF'",
    "blocked_actions_when_not_allow": [
      "BUY",
      "ADD"
    ],
    "unaffected_actions": [
      "HOLD",
      "REDUCE",
      "EXIT"
    ],
    "warning": "Do not recompute gate_state directly from SPX close < SPX MA50. R7 proved the direct formula mismatched legacy target."
  },
  "entry_capacity_contract": {
    "mapping_observed_in_r8": {
      "FULL_ON": 3,
      "CAUTIOUS_ON": 2,
      "CASH_MODE": 0
    },
    "responsibility_boundary": {
      "MarketStateEvaluator": "Computes or receives market_state and entry_capacity using legacy-equivalent upstream rules.",
      "MarketGateEvaluator": "Consumes market_state, entry_capacity, and shock inputs to derive gate decision.",
      "UptrendCore": "Consumes MarketGateDecision to block BUY/ADD only."
    },
    "r10_design_choice": "Keep entry_capacity as an explicit input to MarketGateEvaluator, not an implicit recomputation inside _gate_state."
  },
  "call_chain_integration_contract": {
    "legacy_full_artifact_chain": [
      "run_stateful_simulation",
      "_core_e1r / core_variant_result",
      "build_e1r_sidecar_sleeve",
      "_sidecar_result",
      "compose_e1r_v0_2_variant",
      "E1R_REGIME_AWARE_V0_2"
    ],
    "standalone_target_chain": [
      "HistoricalDataAdapter / ForwardDataAdapter",
      "MarketStateEvaluator",
      "MarketGateEvaluator",
      "UptrendCore",
      "SidewaysCore",
      "RegimeRouter",
      "E1RCoreEngine",
      "BacktestRunner / ForwardRunner"
    ],
    "do_not_mix": [
      "Do not let sidecar Top10 become live holdings > 3.",
      "Do not let SIDEWAYS sidecar change UPTREND gate behavior.",
      "Do not use invalid stitched curves as equivalence target."
    ]
  },
  "equivalence_test_plan": {
    "stage": "future R11/R12, not R10",
    "golden_master_sources": [
      "R7 62-row short-window legacy locals trace",
      "R8 market state parameter audit",
      "R9D source-line matrix"
    ],
    "row_level_assertions": [
      "date exact match",
      "market_state exact match",
      "entry_capacity exact match",
      "market_shock exact match",
      "market_risk_off exact match",
      "market_entry_allowed exact match",
      "gate_state exact match",
      "blocked_actions exact match",
      "unaffected_actions exact match"
    ],
    "pass_threshold": {
      "mismatch_count": 0,
      "required_rows": "all rows in golden master trace"
    }
  },
  "implementation_sequence_after_approval": [
    {
      "stage": "4C-2C-4E-ENGINE-K2-R11-MARKET_GATE_STANDALONE_SKELETON",
      "allowed": "Add dataclasses and evaluator skeleton with no strategy integration."
    },
    {
      "stage": "4C-2C-4E-ENGINE-K2-R12-MARKET_GATE_EQUIVALENCE_SMOKE",
      "allowed": "Compare evaluator output against R7/R8 golden rows."
    },
    {
      "stage": "4C-2C-4E-ENGINE-K2-R13-UPTREND_CORE_GATE_WIRING_PROPOSAL",
      "allowed": "Proposal only for how UptrendCore should consume gate decision."
    }
  ],
  "proposal_risk_controls": [
    "No patch in R10.",
    "No full 5Y run in R10.",
    "No formula simplification.",
    "No candidate/BUY/ADD/REDUCE/EXIT extraction in R10.",
    "No replication-ready implementation until row-level equivalence passes."
  ]
}
```

## Validations
```json
{
  "proposal_complete": true,
  "rca2_loaded": true,
  "r9d_loaded": true,
  "r9d_source_line_evidence_ready": true,
  "r9d_blocking_fields_empty": true,
  "all_required_sections_present": true,
  "market_gate_module_design_present": true,
  "source_equivalent_logic_contract_present": true,
  "entry_capacity_boundary_defined": true,
  "call_chain_integration_contract_present": true,
  "equivalence_test_plan_present": true,
  "implementation_sequence_after_approval_defined": true,
  "strategy_logic_changed": false,
  "audit_only": true,
  "proposal_only": true,
  "formula_not_patched": true,
  "backtest_engine_run": false,
  "short_window_existing_engine_run": false,
  "full_5y_backtest_run": false,
  "forward_runner_run": false,
  "candidate_generation_extracted": false,
  "buy_add_reduce_exit_extracted": false,
  "official_result_generated": false,
  "dashboard_changed": false,
  "strategy_files_unchanged": true,
  "proposed_files_not_created": true
}
```

## Decision
```json
{
  "k2_r10_market_gate_standalone_replication_proposal_passed": true,
  "market_state_115_replication_proposal_ready": true,
  "market_gate_implementation_allowed_now": false,
  "formula_patch_allowed_now": false,
  "candidate_extraction_allowed_now": false,
  "implementation_may_resume": false,
  "requires_user_approval_before_next_implementation_stage": true,
  "next_stage_after_user_approval": "4C-2C-4E-ENGINE-K2-R11-MARKET_GATE_STANDALONE_SKELETON",
  "conclusion": "K2_R10_PASS_PROPOSAL_READY_FOR_USER_REVIEW_BEFORE_R11",
  "recommended_next_action": "Review proposal. If accepted, proceed to R11 skeleton only; still no full strategy extraction."
}
```
