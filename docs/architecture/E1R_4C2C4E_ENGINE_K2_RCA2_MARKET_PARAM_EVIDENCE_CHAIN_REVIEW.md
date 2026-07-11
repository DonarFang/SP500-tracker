# E1R 4C-2C-4E-ENGINE-K2-RCA2 — Market Parameter Evidence Chain Review

Generated At: `2026-07-11T02:55:13.675758+00:00`

## Purpose
Stop after three attempts toward the same objective and perform review/root cause analysis before next market-param evidence step.

## Stop Rule
Three attempts toward the same objective have not reached the final replication evidence standard. Implementation is stopped before the next step.

## Attempt Review
```json
[
  {
    "attempt": "K2-R9-MARKET_STATE_115_RETURN_ARTIFACT_AUDIT",
    "objective": "Find the exact 115% E1R artifact and compare whether it contains market gate parameters.",
    "achieved": {
      "target_artifact_found": true,
      "target_return_verified": true
    },
    "not_achieved": {
      "market_state_115_replication_ready": false,
      "blocking_unresolved": [
        {
          "id": "full_115_artifact_missing_market_entry_gate",
          "field": "market_entry_gate",
          "blocking_for_replication": true
        },
        {
          "id": "full_115_artifact_missing_market_gate_enabled",
          "field": "market_gate_enabled",
          "blocking_for_replication": true
        },
        {
          "id": "full_115_artifact_missing_risk_off_below_spx_ma50",
          "field": "risk_off_below_spx_ma50",
          "blocking_for_replication": true
        },
        {
          "id": "full_115_artifact_missing_market_shock_gate_enabled",
          "field": "market_shock_gate_enabled",
          "blocking_for_replication": true
        },
        {
          "id": "full_115_artifact_missing_market_shock_daily_return",
          "field": "market_shock_daily_return",
          "blocking_for_replication": true
        }
      ]
    },
    "failure_mode": "Target artifact was found, but the summary artifact did not persist the required market gate parameter fields.",
    "evidence_boundary": "Artifact-level summary only; insufficient for parameter identity."
  },
  {
    "attempt": "K2-R9B-115_RETURN_ARTIFACT_RECOVERY",
    "objective": "Recover generator/call-chain candidates and parameter evidence for the 115% artifact.",
    "achieved": {
      "target_artifact_exists": true,
      "target_return_verified": true,
      "repository_grep_completed": true,
      "candidate_script_analysis_completed": true
    },
    "not_achieved": {
      "market_state_115_replication_ready": false,
      "blocking_unresolved": [
        {
          "id": "target_artifact_missing_market_gate_parameters",
          "blocking_for_replication": true
        },
        {
          "id": "full_115_artifact_missing_market_entry_gate",
          "field": "market_entry_gate",
          "blocking_for_replication": true
        },
        {
          "id": "full_115_artifact_missing_market_gate_enabled",
          "field": "market_gate_enabled",
          "blocking_for_replication": true
        },
        {
          "id": "full_115_artifact_missing_risk_off_below_spx_ma50",
          "field": "risk_off_below_spx_ma50",
          "blocking_for_replication": true
        },
        {
          "id": "full_115_artifact_missing_market_shock_gate_enabled",
          "field": "market_shock_gate_enabled",
          "blocking_for_replication": true
        },
        {
          "id": "full_115_artifact_missing_market_shock_daily_return",
          "field": "market_shock_daily_return",
          "blocking_for_replication": true
        }
      ]
    },
    "failure_mode": "Generator candidates were found, but the highest-ranked candidate set included self/audit-script pollution and did not isolate original source-line evidence.",
    "evidence_boundary": "Repository grep and candidate grouping; insufficient pollution controls."
  },
  {
    "attempt": "K2-R9C-115_RETURN_GENERATOR_TRACE",
    "objective": "Parse generator trace and recover clean source/call-chain evidence for market gate parameters.",
    "achieved": {
      "generator_path_trace_exists": true,
      "generator_path_trace_relevant_rows_found": true,
      "target_artifact_exists": true,
      "clean_repo_grep_completed": true
    },
    "not_achieved": {
      "market_state_115_replication_ready_claimed": true,
      "market_entry_gate_evidence_count": 0,
      "source_quality_problem": "Evidence samples still include R9/R9B/R9C audit artifacts and generated reports."
    },
    "failure_mode": "R9C validation accepted evidence counts without distinguishing original source-line evidence from generated audit/report evidence; market_entry_gate was not required.",
    "evidence_boundary": "Term-level evidence count is not equivalent to clean source-line provenance."
  }
]
```

## Current Evidence Status
```json
{
  "blocking_fields": [
    "market_entry_gate",
    "market_gate_enabled",
    "risk_off_below_spx_ma50",
    "market_shock_gate_enabled",
    "market_shock_daily_return"
  ],
  "field_status": {
    "market_entry_gate": {
      "reported_evidence_count": 0,
      "sample_count": 0,
      "clean_sample_count_after_pollution_filter": 0,
      "polluted_sample_count_after_filter": 0,
      "clean_sample_examples": [],
      "polluted_sample_examples": [],
      "requires_source_line_trace": true
    },
    "market_gate_enabled": {
      "reported_evidence_count": 95,
      "sample_count": 20,
      "clean_sample_count_after_pollution_filter": 2,
      "polluted_sample_count_after_filter": 18,
      "clean_sample_examples": [
        {
          "source": "clean_repo_grep",
          "file": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C4B_ORIGINAL_ENTRYPOINT_LOCK_REPORT.json",
          "line": 229,
          "text": "      \"source_head\": \"def run_strategy_variant_comparison(\\n    symbols: list[str],\\n    prices_map: dict[str, list[float]],\\n    dates_map: dict[str, list[str]],\\n    spx_prices: list[float],\\n    spx_dates: list[str],\\n    ndx_prices: list[float] = None,\\n    ndx_dates:  list[str]   = None,\\n    sox_prices: list[float] = None,\\n    sox_dates:  list[str]   = None,\\n    vix_prices: list[float] = None,\\n    vix_dates:  list[str]   = None,\\n) -> dict:\\n    \\\"\\\"\\\"\\n    Run four diagnostic portfolio variants using Strict Top3, no fixed TP.\\n\\n    V0_BASE: current Strict Top3 baseline.\\n    V1_RS95: raise entry RS threshold from 90 to 95.\\n    V2_RS95_MINHOLD5: add minimum 5 trading-day hold for ordinary REDUCE/EXIT.\\n    V3_RS95_MINHOLD5_RELSTOP8: add relative SPX underperformance stop.\\n\\n    Selection policy:\\n    1. Prefer PASS over PARTIAL over FAIL.\\n    2. Within the same status, prefer higher total return.\\n    3. Break ties with higher Profit Factor, higher Sharpe, then lower max drawdown.\\n    \\\"\\\"\\\"\\n    logger.info(\\\"[Backtest Layer D v1.6] Strategy Variant Comparison...\\\")\\n\\n    base = {\\n        **LAYER_D_ASSUMPTIONS,\\n        \\\"market_gate_enabled\\\": False,\\n        \\\"market_shock_gate_enabled\\\": False,\\n        \\\"partial_take_profit_enabled\\\": False,\\n        \\\"block_add_after_take_profit\\\": False,\\n    }\\n    # ── Gate v2 No VIX（冻结市场层基准）─────────────────────────\\n    _gate_v2_no_vix = {\\n        \\\"market_gate_enabled\\\":       True,\\n        \\\"risk_off_below_spx_m"
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C4B_ORIGINAL_ENTRYPOINT_LOCK_REPORT.json",
          "line": 1951,
          "text": "              \"text\": \"    market_gate_enabled = bool(a.get(\\\"market_gate_enabled\\\", True))\""
        }
      ],
      "polluted_sample_examples": [
        {
          "source": "clean_repo_grep",
          "file": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.json",
          "line": 76,
          "text": "          \"market_gate_enabled\","
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.json",
          "line": 192,
          "text": "          \"market_gate_enabled\","
        },
        {
          "source": "clean_repo_grep",
          "file": "exports/e1r_engine/audit/e1r_k2_r9b_115_return_artifact_recovery.json",
          "line": 76,
          "text": "          \"market_gate_enabled\","
        },
        {
          "source": "clean_repo_grep",
          "file": "exports/e1r_engine/audit/e1r_k2_r9b_115_return_artifact_recovery.json",
          "line": 192,
          "text": "          \"market_gate_enabled\","
        },
        {
          "source": "clean_repo_grep",
          "file": "exports/e1r_engine/equivalence/e1r_k2_r9b_115_return_artifact_recovery_evidence.json",
          "line": 76,
          "text": "          \"market_gate_enabled\","
        },
        {
          "source": "clean_repo_grep",
          "file": "exports/e1r_engine/equivalence/e1r_k2_r9b_115_return_artifact_recovery_evidence.json",
          "line": 192,
          "text": "          \"market_gate_enabled\","
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
          "line": 57,
          "text": "        \"market_gate_enabled\","
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
          "line": 175,
          "text": "      \"market_gate_enabled\","
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
          "line": 57,
          "text": "        \"market_gate_enabled\","
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
          "line": 175,
          "text": "      \"market_gate_enabled\","
        }
      ],
      "requires_source_line_trace": true
    },
    "risk_off_below_spx_ma50": {
      "reported_evidence_count": 65,
      "sample_count": 20,
      "clean_sample_count_after_pollution_filter": 2,
      "polluted_sample_count_after_filter": 18,
      "clean_sample_examples": [
        {
          "source": "clean_repo_grep",
          "file": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C4B_ORIGINAL_ENTRYPOINT_LOCK_REPORT.json",
          "line": 229,
          "text": "      \"source_head\": \"def run_strategy_variant_comparison(\\n    symbols: list[str],\\n    prices_map: dict[str, list[float]],\\n    dates_map: dict[str, list[str]],\\n    spx_prices: list[float],\\n    spx_dates: list[str],\\n    ndx_prices: list[float] = None,\\n    ndx_dates:  list[str]   = None,\\n    sox_prices: list[float] = None,\\n    sox_dates:  list[str]   = None,\\n    vix_prices: list[float] = None,\\n    vix_dates:  list[str]   = None,\\n) -> dict:\\n    \\\"\\\"\\\"\\n    Run four diagnostic portfolio variants using Strict Top3, no fixed TP.\\n\\n    V0_BASE: current Strict Top3 baseline.\\n    V1_RS95: raise entry RS threshold from 90 to 95.\\n    V2_RS95_MINHOLD5: add minimum 5 trading-day hold for ordinary REDUCE/EXIT.\\n    V3_RS95_MINHOLD5_RELSTOP8: add relative SPX underperformance stop.\\n\\n    Selection policy:\\n    1. Prefer PASS over PARTIAL over FAIL.\\n    2. Within the same status, prefer higher total return.\\n    3. Break ties with higher Profit Factor, higher Sharpe, then lower max drawdown.\\n    \\\"\\\"\\\"\\n    logger.info(\\\"[Backtest Layer D v1.6] Strategy Variant Comparison...\\\")\\n\\n    base = {\\n        **LAYER_D_ASSUMPTIONS,\\n        \\\"market_gate_enabled\\\": False,\\n        \\\"market_shock_gate_enabled\\\": False,\\n        \\\"partial_take_profit_enabled\\\": False,\\n        \\\"block_add_after_take_profit\\\": False,\\n    }\\n    # ── Gate v2 No VIX（冻结市场层基准）─────────────────────────\\n    _gate_v2_no_vix = {\\n        \\\"market_gate_enabled\\\":       True,\\n        \\\"risk_off_below_spx_m"
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C4B_ORIGINAL_ENTRYPOINT_LOCK_REPORT.json",
          "line": 1955,
          "text": "              \"text\": \"    risk_off_below_spx_ma50 = bool(a.get(\\\"risk_off_below_spx_ma50\\\", True))\""
        }
      ],
      "polluted_sample_examples": [
        {
          "source": "clean_repo_grep",
          "file": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.json",
          "line": 79,
          "text": "          \"risk_off_below_spx_ma50\","
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.json",
          "line": 195,
          "text": "          \"risk_off_below_spx_ma50\","
        },
        {
          "source": "clean_repo_grep",
          "file": "exports/e1r_engine/audit/e1r_k2_r9b_115_return_artifact_recovery.json",
          "line": 79,
          "text": "          \"risk_off_below_spx_ma50\","
        },
        {
          "source": "clean_repo_grep",
          "file": "exports/e1r_engine/audit/e1r_k2_r9b_115_return_artifact_recovery.json",
          "line": 195,
          "text": "          \"risk_off_below_spx_ma50\","
        },
        {
          "source": "clean_repo_grep",
          "file": "exports/e1r_engine/equivalence/e1r_k2_r9b_115_return_artifact_recovery_evidence.json",
          "line": 79,
          "text": "          \"risk_off_below_spx_ma50\","
        },
        {
          "source": "clean_repo_grep",
          "file": "exports/e1r_engine/equivalence/e1r_k2_r9b_115_return_artifact_recovery_evidence.json",
          "line": 195,
          "text": "          \"risk_off_below_spx_ma50\","
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
          "line": 60,
          "text": "        \"risk_off_below_spx_ma50\","
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
          "line": 178,
          "text": "      \"risk_off_below_spx_ma50\","
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
          "line": 60,
          "text": "        \"risk_off_below_spx_ma50\","
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
          "line": 178,
          "text": "      \"risk_off_below_spx_ma50\","
        }
      ],
      "requires_source_line_trace": true
    },
    "market_shock_gate_enabled": {
      "reported_evidence_count": 84,
      "sample_count": 20,
      "clean_sample_count_after_pollution_filter": 2,
      "polluted_sample_count_after_filter": 18,
      "clean_sample_examples": [
        {
          "source": "clean_repo_grep",
          "file": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C4B_ORIGINAL_ENTRYPOINT_LOCK_REPORT.json",
          "line": 229,
          "text": "      \"source_head\": \"def run_strategy_variant_comparison(\\n    symbols: list[str],\\n    prices_map: dict[str, list[float]],\\n    dates_map: dict[str, list[str]],\\n    spx_prices: list[float],\\n    spx_dates: list[str],\\n    ndx_prices: list[float] = None,\\n    ndx_dates:  list[str]   = None,\\n    sox_prices: list[float] = None,\\n    sox_dates:  list[str]   = None,\\n    vix_prices: list[float] = None,\\n    vix_dates:  list[str]   = None,\\n) -> dict:\\n    \\\"\\\"\\\"\\n    Run four diagnostic portfolio variants using Strict Top3, no fixed TP.\\n\\n    V0_BASE: current Strict Top3 baseline.\\n    V1_RS95: raise entry RS threshold from 90 to 95.\\n    V2_RS95_MINHOLD5: add minimum 5 trading-day hold for ordinary REDUCE/EXIT.\\n    V3_RS95_MINHOLD5_RELSTOP8: add relative SPX underperformance stop.\\n\\n    Selection policy:\\n    1. Prefer PASS over PARTIAL over FAIL.\\n    2. Within the same status, prefer higher total return.\\n    3. Break ties with higher Profit Factor, higher Sharpe, then lower max drawdown.\\n    \\\"\\\"\\\"\\n    logger.info(\\\"[Backtest Layer D v1.6] Strategy Variant Comparison...\\\")\\n\\n    base = {\\n        **LAYER_D_ASSUMPTIONS,\\n        \\\"market_gate_enabled\\\": False,\\n        \\\"market_shock_gate_enabled\\\": False,\\n        \\\"partial_take_profit_enabled\\\": False,\\n        \\\"block_add_after_take_profit\\\": False,\\n    }\\n    # ── Gate v2 No VIX（冻结市场层基准）─────────────────────────\\n    _gate_v2_no_vix = {\\n        \\\"market_gate_enabled\\\":       True,\\n        \\\"risk_off_below_spx_m"
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C4B_ORIGINAL_ENTRYPOINT_LOCK_REPORT.json",
          "line": 2095,
          "text": "              \"text\": \"    market_shock_gate_enabled = bool(a.get(\\\"market_shock_gate_enabled\\\", True))\""
        }
      ],
      "polluted_sample_examples": [
        {
          "source": "clean_repo_grep",
          "file": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.json",
          "line": 78,
          "text": "          \"market_shock_gate_enabled\","
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.json",
          "line": 194,
          "text": "          \"market_shock_gate_enabled\","
        },
        {
          "source": "clean_repo_grep",
          "file": "exports/e1r_engine/audit/e1r_k2_r9b_115_return_artifact_recovery.json",
          "line": 78,
          "text": "          \"market_shock_gate_enabled\","
        },
        {
          "source": "clean_repo_grep",
          "file": "exports/e1r_engine/audit/e1r_k2_r9b_115_return_artifact_recovery.json",
          "line": 194,
          "text": "          \"market_shock_gate_enabled\","
        },
        {
          "source": "clean_repo_grep",
          "file": "exports/e1r_engine/equivalence/e1r_k2_r9b_115_return_artifact_recovery_evidence.json",
          "line": 78,
          "text": "          \"market_shock_gate_enabled\","
        },
        {
          "source": "clean_repo_grep",
          "file": "exports/e1r_engine/equivalence/e1r_k2_r9b_115_return_artifact_recovery_evidence.json",
          "line": 194,
          "text": "          \"market_shock_gate_enabled\","
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
          "line": 59,
          "text": "        \"market_shock_gate_enabled\","
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
          "line": 177,
          "text": "      \"market_shock_gate_enabled\","
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
          "line": 59,
          "text": "        \"market_shock_gate_enabled\","
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
          "line": 177,
          "text": "      \"market_shock_gate_enabled\","
        }
      ],
      "requires_source_line_trace": true
    },
    "market_shock_daily_return": {
      "reported_evidence_count": 81,
      "sample_count": 20,
      "clean_sample_count_after_pollution_filter": 2,
      "polluted_sample_count_after_filter": 18,
      "clean_sample_examples": [
        {
          "source": "clean_repo_grep",
          "file": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C4B_ORIGINAL_ENTRYPOINT_LOCK_REPORT.json",
          "line": 229,
          "text": "      \"source_head\": \"def run_strategy_variant_comparison(\\n    symbols: list[str],\\n    prices_map: dict[str, list[float]],\\n    dates_map: dict[str, list[str]],\\n    spx_prices: list[float],\\n    spx_dates: list[str],\\n    ndx_prices: list[float] = None,\\n    ndx_dates:  list[str]   = None,\\n    sox_prices: list[float] = None,\\n    sox_dates:  list[str]   = None,\\n    vix_prices: list[float] = None,\\n    vix_dates:  list[str]   = None,\\n) -> dict:\\n    \\\"\\\"\\\"\\n    Run four diagnostic portfolio variants using Strict Top3, no fixed TP.\\n\\n    V0_BASE: current Strict Top3 baseline.\\n    V1_RS95: raise entry RS threshold from 90 to 95.\\n    V2_RS95_MINHOLD5: add minimum 5 trading-day hold for ordinary REDUCE/EXIT.\\n    V3_RS95_MINHOLD5_RELSTOP8: add relative SPX underperformance stop.\\n\\n    Selection policy:\\n    1. Prefer PASS over PARTIAL over FAIL.\\n    2. Within the same status, prefer higher total return.\\n    3. Break ties with higher Profit Factor, higher Sharpe, then lower max drawdown.\\n    \\\"\\\"\\\"\\n    logger.info(\\\"[Backtest Layer D v1.6] Strategy Variant Comparison...\\\")\\n\\n    base = {\\n        **LAYER_D_ASSUMPTIONS,\\n        \\\"market_gate_enabled\\\": False,\\n        \\\"market_shock_gate_enabled\\\": False,\\n        \\\"partial_take_profit_enabled\\\": False,\\n        \\\"block_add_after_take_profit\\\": False,\\n    }\\n    # ── Gate v2 No VIX（冻结市场层基准）─────────────────────────\\n    _gate_v2_no_vix = {\\n        \\\"market_gate_enabled\\\":       True,\\n        \\\"risk_off_below_spx_m"
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C4B_ORIGINAL_ENTRYPOINT_LOCK_REPORT.json",
          "line": 3024,
          "text": "              \"text\": \"        \\\"market_shock_daily_return\\\": -0.02,\""
        }
      ],
      "polluted_sample_examples": [
        {
          "source": "clean_repo_grep",
          "file": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.json",
          "line": 77,
          "text": "          \"market_shock_daily_return\","
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.json",
          "line": 193,
          "text": "          \"market_shock_daily_return\","
        },
        {
          "source": "clean_repo_grep",
          "file": "exports/e1r_engine/audit/e1r_k2_r9b_115_return_artifact_recovery.json",
          "line": 77,
          "text": "          \"market_shock_daily_return\","
        },
        {
          "source": "clean_repo_grep",
          "file": "exports/e1r_engine/audit/e1r_k2_r9b_115_return_artifact_recovery.json",
          "line": 193,
          "text": "          \"market_shock_daily_return\","
        },
        {
          "source": "clean_repo_grep",
          "file": "exports/e1r_engine/equivalence/e1r_k2_r9b_115_return_artifact_recovery_evidence.json",
          "line": 77,
          "text": "          \"market_shock_daily_return\","
        },
        {
          "source": "clean_repo_grep",
          "file": "exports/e1r_engine/equivalence/e1r_k2_r9b_115_return_artifact_recovery_evidence.json",
          "line": 193,
          "text": "          \"market_shock_daily_return\","
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
          "line": 58,
          "text": "        \"market_shock_daily_return\","
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
          "line": 176,
          "text": "      \"market_shock_daily_return\","
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
          "line": 58,
          "text": "        \"market_shock_daily_return\","
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
          "line": 176,
          "text": "      \"market_shock_daily_return\","
        }
      ],
      "requires_source_line_trace": true
    }
  },
  "generator_trace_file": {
    "exists": true,
    "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0D_GENERATOR_PATH_TRACE.json",
    "sha256": "5944e610222879e27dd99515fad747febfcdb2da12a0abc89d6ff861e55d41cd"
  },
  "target_artifact": {
    "exists": true,
    "path": "exports/e1r_v0_2_backtest_summary.json",
    "sha256": "449a8ace55ce2335d174e17e2532d8793a3a9b99c021a935f8d7f2e531092114"
  }
}
```

## Root Cause Analysis
```json
{
  "three_attempt_stop_rule_triggered": true,
  "repeated_objective": "Recover source-quality evidence proving the 115% E1R v0.2 market gate / market state parameter chain before standalone replication.",
  "attempts_counted": [
    "K2-R9",
    "K2-R9B",
    "K2-R9C"
  ],
  "what_is_known": [
    "The 115% / 116.7435999134756 E1R artifact exists at exports/e1r_v0_2_backtest_summary.json.",
    "The target artifact identifies strategy_id E1R_REGIME_AWARE_V0_2.",
    "The target artifact identifies regime_aware_logic as UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE.",
    "The sidecar was active in SIDEWAYS / MA_CONFLICT for 135 rows in the target artifact.",
    "Short-window R8 parameter audit found D3_RISK_OFF_PLUS_SHOCK_GATE, market_gate_enabled=True, risk_off_below_spx_ma50=True, market_shock_gate_enabled=True, market_shock_daily_return=-0.02.",
    "R7/R8 short-window evidence is source-equivalent for the short-window golden master, but does not by itself prove the full 115% artifact parameter identity."
  ],
  "what_is_not_yet_proven": [
    "The full 115% E1R v0.2 artifact itself does not persist market_entry_gate or the required market gate parameter fields.",
    "The original generator source-line chain for each market gate parameter has not been cleanly isolated.",
    "Evidence counts in R9C include generated audit/report artifacts and therefore cannot be accepted as source-line proof.",
    "market_entry_gate had zero evidence in R9C and was not included as a required blocking condition."
  ],
  "root_causes": [
    {
      "id": "RC1_EVIDENCE_COUNT_OVER_SOURCE_PROVENANCE",
      "description": "R9C treated term evidence count as sufficient, but did not require original source-line provenance.",
      "impact": "Generated audit/report files could satisfy evidence_count without proving the real generator code path."
    },
    {
      "id": "RC2_INCOMPLETE_POLLUTION_FILTER",
      "description": "R9B/R9C excluded some self-reference scripts but did not exclude all generated audit/research/equivalence artifacts.",
      "impact": "Evidence samples were contaminated by prior audit outputs."
    },
    {
      "id": "RC3_REQUIRED_FIELD_SET_INCOMPLETE",
      "description": "R9C did not require market_entry_gate or an explicitly equivalent output structure as a blocking field.",
      "impact": "market_state_115_replication_ready could become true despite market_entry_gate evidence_count=0."
    },
    {
      "id": "RC4_SHORT_WINDOW_AND_FULL_ARTIFACT_BOUNDARY",
      "description": "R8 short-window parameters are strong but cannot be automatically promoted to full 115% artifact identity.",
      "impact": "A separate full artifact generator/source-line trace is still required."
    },
    {
      "id": "RC5_GENERATOR_TRACE_JSON_IS_A_TRACE_INDEX_NOT_DIRECT_PROOF",
      "description": "The generator trace JSON points to candidate files and source fragments, but it is not itself the original generator implementation.",
      "impact": "The next step must inspect original source files / source_head / source lines, not accept the trace index as final proof."
    }
  ],
  "corrective_principles": [
    "Do not proceed to implementation or replication proposal until each blocking field has clean source-line evidence.",
    "Evidence must be classified by quality: original source code > original generator artifact with source_head/source_line > runtime trace > generated audit report.",
    "Generated docs/research/E1R_4C2C4E_ENGINE_K2_* and exports/e1r_engine/* must be excluded from source proof.",
    "market_entry_gate must be either found directly or explicitly mapped to an equivalent source structure.",
    "A PASS can mean RCA complete; it must not imply replication_ready unless all blocking evidence gates are satisfied."
  ]
}
```

## Corrective Plan
```json
{
  "next_stage": "4C-2C-4E-ENGINE-K2-R9D-MARKET_PARAM_SOURCE_LINE_TRACE",
  "stage_type": "source-line audit only",
  "allowed": [
    "Read existing source files and existing generator trace artifacts.",
    "Extract source-line snippets for market gate parameters.",
    "Classify evidence quality.",
    "Produce a field-by-field evidence matrix.",
    "Commit only audit/report/script files."
  ],
  "not_allowed": [
    "No strategy logic patch.",
    "No full 5Y backtest.",
    "No short-window rerun unless explicitly approved.",
    "No candidate/BUY/ADD/REDUCE/EXIT extraction.",
    "No official result or dashboard change.",
    "No replication proposal until R9D passes source-line evidence gates."
  ],
  "mandatory_source_filter": {
    "include_preferred": [
      "src/engine/backtest.py",
      "src/engine/e1r_composer.py",
      "src/engine/e1r_sidecar_sleeve.py",
      "original generator candidate source files referenced by E1R_V0_2_STAGE3_8E2F2C4C10F4B0D_GENERATOR_PATH_TRACE.json"
    ],
    "exclude_as_primary_proof": [
      "docs/research/E1R_4C2C4E_ENGINE_K2_*.json",
      "docs/research/E1R_4C2C4E_ENGINE_K2_*.md",
      "docs/architecture/E1R_4C2C4E_ENGINE_K2_*.md",
      "exports/e1r_engine/audit/*.json",
      "exports/e1r_engine/equivalence/*.json",
      "scripts/e1r_k2_r9*.py",
      "scripts/e1r_k2_rca*.py"
    ]
  },
  "required_evidence_matrix_fields": [
    {
      "field": "market_gate_enabled",
      "required": "source line or source_head showing assignment/default and call-path into run_stateful_simulation assumptions for E1R v0.2 core"
    },
    {
      "field": "risk_off_below_spx_ma50",
      "required": "source line or source_head showing assignment/default and usage in market_state / entry_capacity / risk-off logic"
    },
    {
      "field": "market_shock_gate_enabled",
      "required": "source line or source_head showing assignment/default and usage in _shock_active"
    },
    {
      "field": "market_shock_daily_return",
      "required": "source line or source_head showing assignment/default value -0.02 and usage in _shock_active"
    },
    {
      "field": "market_entry_gate_or_equivalent",
      "required": "source evidence showing output structure or explicit equivalent: blocked BUY/ADD, unaffected HOLD/REDUCE/EXIT, entry_capacity mapping, or generated market gate report"
    },
    {
      "field": "e1r_v0_2_core_call_chain",
      "required": "source evidence showing run_stateful_simulation -> core_variant_result/_core_e1r -> compose_e1r_v0_2_variant"
    },
    {
      "field": "e1r_v0_2_sidecar_call_chain",
      "required": "source evidence showing build_e1r_sidecar_sleeve -> sidecar_result -> compose_e1r_v0_2_variant, MA_CONFLICT 135-row sleeve"
    }
  ],
  "pass_conditions_for_r9d": [
    "Every required evidence matrix field is PASS or explicitly documented as equivalent with source-line proof.",
    "No blocking field relies only on generated audit/report/equivalence files.",
    "R8 short-window parameters are treated as supporting evidence, not sole proof for full 115% artifact.",
    "market_state_115_replication_ready remains false unless all source-line evidence gates pass.",
    "formula_patch_allowed_now remains false."
  ]
}
```

## Validations
```json
{
  "rca2_review_complete": true,
  "three_attempt_stop_rule_triggered": true,
  "repeated_objective_identified": true,
  "attempts_reviewed_count": 3,
  "r9_loaded": true,
  "r9b_loaded": true,
  "r9c_loaded": true,
  "r8_loaded": true,
  "evidence_vs_assumption_separated": true,
  "root_causes_identified": true,
  "corrective_plan_defined": true,
  "strategy_logic_changed": false,
  "audit_only": true,
  "formula_not_patched": true,
  "backtest_engine_run": false,
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
  "k2_rca2_market_param_evidence_chain_review_passed": true,
  "implementation_may_resume": false,
  "market_state_115_replication_ready": false,
  "formula_patch_allowed_now": false,
  "candidate_extraction_allowed_now": false,
  "next_required_stage": "4C-2C-4E-ENGINE-K2-R9D-MARKET_PARAM_SOURCE_LINE_TRACE",
  "conclusion": "K2_RCA2_PASS_STOP_CONFIRMED_READY_FOR_R9D_SOURCE_LINE_TRACE_ONLY",
  "recommended_next_action": "Proceed only to R9D source-line trace with strict pollution filters and field-by-field evidence gates. Do not implement or patch."
}
```
