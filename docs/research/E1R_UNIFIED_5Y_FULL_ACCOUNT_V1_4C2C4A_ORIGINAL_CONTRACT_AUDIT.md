# E1R Combined 5Y — 4C-2C-4A Original Contract Recovery Audit

Generated At: `2026-07-09T12:57:24.427839+00:00`

## Policy

```json
{
  "strategy_logic_changed": false,
  "backtest_run": false,
  "dashboard_changed": false,
  "exports_modified": false,
  "purpose": "Recover and verify original E1R contract before combined 5Y run."
}
```

## Frozen User Contract

```json
{
  "strategy_id": "E1R_COMBINED_5Y_ORIGINAL_CONTRACT",
  "rules": [
    "UPTREND uses the previously validated UPTREND strategy.",
    "SIDEWAYS / MA_CONFLICT uses the previously validated sidecar strategy.",
    "DETERIORATION / RECOVERY participates only if confirmed by original SIDEWAYS definition; otherwise cash/defensive.",
    "DOWNTREND is cash/defensive.",
    "Actual account holdings must always be <= 3 stocks in every regime.",
    "SIDEWAYS Top10 is candidate pool only, not 10 live account holdings.",
    "No trading strategy logic changes are allowed in this audit."
  ]
}
```

## Scan Summary

```json
{
  "files_with_hits": 272,
  "top_files": [
    {
      "path": "scripts/audit_e1r_original_contract_4c2c4a.py",
      "score": 225,
      "groups": [
        "deterioration_recovery",
        "downtrend",
        "known_invalid_max10",
        "position_cap",
        "sideways_sidecar",
        "top10_candidate_pool",
        "uptrend_confirmed",
        "uptrend_emerging"
      ],
      "hit_count": 103
    },
    {
      "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C1_PREFLIGHT_REPORT.json",
      "score": 195,
      "groups": [
        "deterioration_recovery",
        "downtrend",
        "position_cap",
        "sideways_sidecar",
        "top10_candidate_pool",
        "uptrend_confirmed",
        "uptrend_emerging"
      ],
      "hit_count": 230
    },
    {
      "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10A_DIRECT_GENERATOR_FUNCTION_AUDIT.json",
      "score": 195,
      "groups": [
        "downtrend",
        "position_cap",
        "sideways_sidecar",
        "top10_candidate_pool",
        "uptrend_confirmed",
        "uptrend_emerging"
      ],
      "hit_count": 179
    },
    {
      "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0_E1_E1R_CORE_CONTRACT_AUDIT.json",
      "score": 195,
      "groups": [
        "downtrend",
        "position_cap",
        "sideways_sidecar",
        "top10_candidate_pool",
        "uptrend_confirmed",
        "uptrend_emerging"
      ],
      "hit_count": 145
    },
    {
      "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0_E1_E1R_CORE_CONTRACT_AUDIT.md",
      "score": 195,
      "groups": [
        "downtrend",
        "position_cap",
        "sideways_sidecar",
        "uptrend_confirmed",
        "uptrend_emerging"
      ],
      "hit_count": 73
    },
    {
      "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C2_RECOVER_5Y_PORTFOLIO_EQUITY_CANDIDATES.json",
      "score": 195,
      "groups": [
        "downtrend",
        "position_cap",
        "sideways_sidecar",
        "top10_candidate_pool",
        "uptrend_confirmed",
        "uptrend_emerging"
      ],
      "hit_count": 297
    },
    {
      "path": "docs/research/stage3_2_backtest_snapshots/backtest_feature_source_stage3_2.py",
      "score": 195,
      "groups": [
        "downtrend",
        "position_cap",
        "sideways_sidecar",
        "top10_candidate_pool",
        "uptrend_confirmed",
        "uptrend_emerging"
      ],
      "hit_count": 190
    },
    {
      "path": "src/engine/backtest.py",
      "score": 195,
      "groups": [
        "downtrend",
        "position_cap",
        "sideways_sidecar",
        "top10_candidate_pool",
        "uptrend_confirmed",
        "uptrend_emerging"
      ],
      "hit_count": 190
    },
    {
      "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C3FD_MARKET_STATE_GENERATOR_AUDIT.json",
      "score": 190,
      "groups": [
        "downtrend",
        "position_cap",
        "sideways_sidecar",
        "uptrend_confirmed",
        "uptrend_emerging"
      ],
      "hit_count": 113
    },
    {
      "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2A_ENGINE_ENTRYPOINT_REPORT.json",
      "score": 175,
      "groups": [
        "deterioration_recovery",
        "downtrend",
        "position_cap",
        "sideways_sidecar",
        "top10_candidate_pool",
        "uptrend_confirmed",
        "uptrend_emerging"
      ],
      "hit_count": 268
    },
    {
      "path": "docs/research/E1R_V0_2_STAGE3_8E2A_DATA_SHAPE_AUDIT.json",
      "score": 175,
      "groups": [
        "downtrend",
        "position_cap",
        "sideways_sidecar",
        "top10_candidate_pool",
        "uptrend_confirmed",
        "uptrend_emerging"
      ],
      "hit_count": 329
    },
    {
      "path": "docs/research/E1R_V0_2_STAGE3_8E2F0_FORWARD_KICKOFF_AUDIT.json",
      "score": 175,
      "groups": [
        "downtrend",
        "position_cap",
        "sideways_sidecar",
        "uptrend_confirmed",
        "uptrend_emerging"
      ],
      "hit_count": 137
    },
    {
      "path": "docs/research/E1R_V0_2_STAGE3_8E2F1A_FORWARD_SOURCE_AUDIT.json",
      "score": 175,
      "groups": [
        "downtrend",
        "position_cap",
        "sideways_sidecar",
        "uptrend_confirmed"
      ],
      "hit_count": 172
    },
    {
      "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C3FB_TREND_REGIME_SOURCE_AUDIT.json",
      "score": 175,
      "groups": [
        "deterioration_recovery",
        "downtrend",
        "position_cap",
        "sideways_sidecar",
        "top10_candidate_pool",
        "uptrend_confirmed",
        "uptrend_emerging"
      ],
      "hit_count": 166
    },
    {
      "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10E_R_CONTINUOUS_CAPITAL_CONTRACT.json",
      "score": 175,
      "groups": [
        "downtrend",
        "position_cap",
        "sideways_sidecar",
        "top10_candidate_pool",
        "uptrend_confirmed",
        "uptrend_emerging"
      ],
      "hit_count": 268
    },
    {
      "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F3B_E1_STATEFUL_WRAPPER_PROBE.json",
      "score": 175,
      "groups": [
        "downtrend",
        "position_cap",
        "sideways_sidecar",
        "top10_candidate_pool",
        "uptrend_confirmed"
      ],
      "hit_count": 16
    },
    {
      "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F3B_E1_STATEFUL_WRAPPER_PROBE.md",
      "score": 175,
      "groups": [
        "downtrend",
        "position_cap",
        "sideways_sidecar",
        "top10_candidate_pool",
        "uptrend_confirmed"
      ],
      "hit_count": 48
    },
    {
      "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0D_GENERATOR_PATH_TRACE.json",
      "score": 175,
      "groups": [
        "deterioration_recovery",
        "downtrend",
        "position_cap",
        "sideways_sidecar",
        "top10_candidate_pool",
        "uptrend_confirmed",
        "uptrend_emerging"
      ],
      "hit_count": 366
    },
    {
      "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0G_GENERATOR_COMPOSER_CONTRACT_AUDIT.json",
      "score": 175,
      "groups": [
        "downtrend",
        "position_cap",
        "sideways_sidecar",
        "top10_candidate_pool",
        "uptrend_confirmed",
        "uptrend_emerging"
      ],
      "hit_count": 111
    },
    {
      "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C3_BACKTEST_GENERATOR_CANONICAL_EXPORT_PLAN.json",
      "score": 175,
      "groups": [
        "downtrend",
        "position_cap",
        "sideways_sidecar",
        "uptrend_confirmed",
        "uptrend_emerging"
      ],
      "hit_count": 203
    },
    {
      "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C6_INTERVAL_SCHEMA_SOURCE_AUDIT.json",
      "score": 175,
      "groups": [
        "deterioration_recovery",
        "downtrend",
        "position_cap",
        "sideways_sidecar",
        "top10_candidate_pool",
        "uptrend_confirmed",
        "uptrend_emerging"
      ],
      "hit_count": 223
    },
    {
      "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json",
      "score": 175,
      "groups": [
        "deterioration_recovery",
        "downtrend",
        "position_cap",
        "sideways_sidecar",
        "top10_candidate_pool",
        "uptrend_confirmed",
        "uptrend_emerging"
      ],
      "hit_count": 346
    },
    {
      "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C3FA_MARKET_STATE_FIELD_AUDIT.json",
      "score": 170,
      "groups": [
        "downtrend",
        "position_cap",
        "sideways_sidecar"
      ],
      "hit_count": 67
    },
    {
      "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0G_GENERATOR_COMPOSER_CONTRACT_AUDIT.md",
      "score": 170,
      "groups": [
        "downtrend",
        "position_cap",
        "sideways_sidecar",
        "top10_candidate_pool"
      ],
      "hit_count": 91
    },
    {
      "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0I_COMPOSER_INPUT_CANDIDATES.json",
      "score": 170,
      "groups": [
        "deterioration_recovery",
        "downtrend",
        "position_cap",
        "sideways_sidecar",
        "top10_candidate_pool",
        "uptrend_confirmed"
      ],
      "hit_count": 229
    }
  ]
}
```

## Findings

```json
[
  {
    "topic": "UPTREND strategy",
    "current_confidence": "NEEDS_SOURCE_CONFIRMATION",
    "expected_contract": "Use previously validated UPTREND strategy. Do not replace with new logic.",
    "evidence_groups": [
      "uptrend_confirmed",
      "uptrend_emerging",
      "position_cap"
    ],
    "audit_question": "Which file/function is the validated UPTREND execution entrypoint?"
  },
  {
    "topic": "SIDEWAYS / MA_CONFLICT strategy",
    "current_confidence": "NEEDS_SOURCE_CONFIRMATION",
    "expected_contract": "Use previously validated SIDEWAYS / MA_CONFLICT sidecar strategy. Top10 is candidate pool only.",
    "evidence_groups": [
      "sideways_sidecar",
      "top10_candidate_pool",
      "deterioration_recovery"
    ],
    "audit_question": "Which file/function/artifact is the validated sidecar execution contract?"
  },
  {
    "topic": "DETERIORATION / RECOVERY",
    "current_confidence": "UNKNOWN_UNTIL_ORIGINAL_SIDEWAYS_CONTRACT_CONFIRMED",
    "expected_contract": "Participate only if original SIDEWAYS strategy explicitly includes them; otherwise cash/defensive.",
    "evidence_groups": [
      "deterioration_recovery"
    ],
    "audit_question": "Were DETERIORATION_TRANSITION or RECOVERY_TRANSITION included in validated SIDEWAYS execution, or only MA_CONFLICT?"
  },
  {
    "topic": "DOWNTREND",
    "current_confidence": "NEEDS_SOURCE_CONFIRMATION",
    "expected_contract": "Cash / defensive.",
    "evidence_groups": [
      "downtrend"
    ],
    "audit_question": "Confirm DOWNTREND has no normal buy execution in combined E1R."
  },
  {
    "topic": "Global account position cap",
    "current_confidence": "USER_FROZEN_CONTRACT",
    "expected_contract": "Actual account holdings <= 3 stocks in every regime.",
    "evidence_groups": [
      "position_cap",
      "known_invalid_max10"
    ],
    "audit_question": "Confirm current combined backtest call enforces account open_positions_count <= 3, not only candidate count."
  }
]
```

## Contract Signals

```json
{
  "uptrend_confirmed": [
    {
      "path": "scripts/audit_e1r_original_contract_4c2c4a.py",
      "score": 225,
      "hits": [
        {
          "line": 47,
          "pattern": "E1R_UPTREND_CONFIRMED",
          "text": "\"E1R_UPTREND_CONFIRMED\","
        },
        {
          "line": 47,
          "pattern": "UPTREND_CONFIRMED",
          "text": "\"E1R_UPTREND_CONFIRMED\","
        },
        {
          "line": 48,
          "pattern": "UPTREND_CONFIRMED",
          "text": "\"UPTREND_CONFIRMED\","
        },
        {
          "line": 49,
          "pattern": "Confirmed",
          "text": "\"Confirmed\","
        },
        {
          "line": 50,
          "pattern": "leader_rank",
          "text": "\"leader_rank\","
        },
        {
          "line": 51,
          "pattern": "leader_score",
          "text": "\"leader_score\","
        },
        {
          "line": 52,
          "pattern": "momentum_acceleration",
          "text": "\"momentum_acceleration\","
        },
        {
          "line": 53,
          "pattern": "rs_20d_improvement",
          "text": "\"rs_20d_improvement\","
        }
      ]
    },
    {
      "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C1_PREFLIGHT_REPORT.json",
      "score": 195,
      "hits": [
        {
          "line": 2254,
          "pattern": "leader_rank",
          "text": "\"text\": \"            leader_rank_all = {s: i + 1 for i, (s, _) in enumerate(top_ranked)}\""
        },
        {
          "line": 2286,
          "pattern": "leader_rank",
          "text": "\"text\": \"            leader_rank_all = {s: i + 1 for i, (s, _) in enumerate(top_ranked)}\""
        },
        {
          "line": 2318,
          "pattern": "leader_rank",
          "text": "\"text\": \"            leader_rank_all = {s: i + 1 for i, (s, _) in enumerate(top_ranked)}\""
        },
        {
          "line": 2326,
          "pattern": "leader_rank",
          "text": "\"text\": \"                rank_all = leader_rank_all.get(sym, 9999)\""
        },
        {
          "line": 2350,
          "pattern": "E1R_UPTREND_CONFIRMED",
          "text": "\"text\": \"                    entry_type = \\\"E1R_UPTREND_CONFIRMED\\\" if confirmed else \\\"E1R_UPTREND_EMERGING\\\"\""
        },
        {
          "line": 2350,
          "pattern": "UPTREND_CONFIRMED",
          "text": "\"text\": \"                    entry_type = \\\"E1R_UPTREND_CONFIRMED\\\" if confirmed else \\\"E1R_UPTREND_EMERGING\\\"\""
        },
        {
          "line": 2495,
          "pattern": "E1R_UPTREND_CONFIRMED",
          "text": "\"text\": \"                _priority = 0 if _etype == \\\"E1R_UPTREND_CONFIRMED\\\" else 1\""
        },
        {
          "line": 2495,
          "pattern": "UPTREND_CONFIRMED",
          "text": "\"text\": \"                _priority = 0 if _etype == \\\"E1R_UPTREND_CONFIRMED\\\" else 1\""
        },
        {
          "line": 2507,
          "pattern": "leader_rank",
          "text": "\"text\": \"                    leader_rank_all.get(s, 9999),\""
        },
        {
          "line": 2531,
          "pattern": "E1R_UPTREND_CONFIRMED",
          "text": "\"text\": \"                        \\\"target_size_units\\\": 1.0 if _etype == \\\"E1R_UPTREND_CONFIRMED\\\" else 0.5,\""
        },
        {
          "line": 2531,
          "pattern": "UPTREND_CONFIRMED",
          "text": "\"text\": \"                        \\\"target_size_units\\\": 1.0 if _etype == \\\"E1R_UPTREND_CONFIRMED\\\" else 0.5,\""
        },
        {
          "line": 2563,
          "pattern": "leader_rank",
          "text": "\"text\": \"                    \\\"entry_rank\\\":     top_entry_rank.get(sym) or leader_rank_all.get(sym),\""
        },
        {
          "line": 2591,
          "pattern": "Confirmed",
          "text": "\"text\": \"        # E1-R Phase 3B: Emerging → Confirmed upgrade ADD.\""
        },
        {
          "line": 2663,
          "pattern": "leader_score",
          "text": "\"text\": \"                    \\\"ls\\\": sig.get(\\\"leader_score\\\", h.get(\\\"leader_score_entry\\\", 0)),\""
        },
        {
          "line": 2671,
          "pattern": "leader_rank",
          "text": "\"text\": \"                    \\\"entry_rank\\\": top_entry_rank.get(sym) or leader_rank_all.get(sym),\""
        },
        {
          "line": 2683,
          "pattern": "momentum_acceleration",
          "text": "\"text\": \"                    \\\"reasons\\\": [\\\"emerging_upgraded_to_confirmed\\\", \\\"position_return_above_3pct\\\", \\\"close_above_ma20\\\", \\\"momentum_acceleration_non_negative\\\"],\""
        },
        {
          "line": 2687,
          "pattern": "E1R_UPTREND_CONFIRMED",
          "text": "\"text\": \"                    \\\"e1r_entry_type\\\": \\\"E1R_UPTREND_CONFIRMED\\\",\""
        },
        {
          "line": 2687,
          "pattern": "UPTREND_CONFIRMED",
          "text": "\"text\": \"                    \\\"e1r_entry_type\\\": \\\"E1R_UPTREND_CONFIRMED\\\",\""
        },
        {
          "line": 2707,
          "pattern": "momentum_acceleration",
          "text": "\"text\": \"                    \\\"reasons\\\": [\\\"emerging_upgraded_to_confirmed\\\", \\\"position_return_above_3pct\\\", \\\"close_above_ma20\\\", \\\"momentum_acceleration_non_negative\\\"],\""
        },
        {
          "line": 2711,
          "pattern": "E1R_UPTREND_CONFIRMED",
          "text": "\"text\": \"                    \\\"e1r_entry_type\\\": \\\"E1R_UPTREND_CONFIRMED\\\",\""
        }
      ]
    },
    {
      "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10A_DIRECT_GENERATOR_FUNCTION_AUDIT.json",
      "score": 195,
      "hits": [
        {
          "line": 3078,
          "pattern": "momentum_acceleration",
          "text": "\"text\": \"from ..features.momentum import momentum_score as calc_momentum, moving_average, linreg_slope, momentum_acceleration\""
        },
        {
          "line": 3086,
          "pattern": "leader_rank",
          "text": "\"text\": \"from ..engine.leader_ranking import leader_score as calc_leader_score\""
        },
        {
          "line": 3086,
          "pattern": "leader_score",
          "text": "\"text\": \"from ..engine.leader_ranking import leader_score as calc_leader_score\""
        },
        {
          "line": 3255,
          "pattern": "leader_score",
          "text": "\"source_head\": \"def run_action_forward_validation(\\n    symbols:       list[str],\\n    prices_map:    dict[str, list[float]],\\n    spx_prices:    list[float],\\n    dates_map:     dict[str, list[str]] | None = None,\\n    spx_dates:     list[str] | None = None,\\n    forward_days:  list[int] = [5, 10, "
        },
        {
          "line": 3275,
          "pattern": "leader_score",
          "text": "\"source_head\": \"def run_trade_rule_validation(\\n    symbols: list[str],\\n    prices_map: dict[str, list[float]],\\n    spx_prices: list[float],\\n    forward_days: list[int] = [5, 10, 20, 30],\\n    step: int = 5,\\n    min_history: int = 120,\\n    market_score_default: float = 60.0,\\n) -> dict:\\n    \\\""
        },
        {
          "line": 3295,
          "pattern": "leader_score",
          "text": "\"source_head\": \"def run_promotion_engine_validation(\\n    symbols: list[str],\\n    prices_map: dict[str, list[float]],\\n    spx_prices: list[float],\\n    promotion_thresholds: list[int] = [80, 85, 90],\\n    track_days: list[int] = [5, 10, 20, 30],\\n    step: int = 5,\\n    min_history: int = 120,\\n) "
        },
        {
          "line": 3426,
          "pattern": "leader_score",
          "text": "\"name\": \"_rebuild_leader_score\","
        },
        {
          "line": 3438,
          "pattern": "leader_score",
          "text": "\"source_head\": \"def _rebuild_leader_score(prices: list[float], spx_prices: list[float],\\n                           all_stocks_prices: dict[str, list[float]],\\n                           t: int) -> dict | None:\\n    \\\"\\\"\\\"\\n    在时间点 t 重建该股票的所有指标（无前视偏差）。\\n    \\\"\\\"\\\"\\n    p = prices[:t+1]\\n    spx = s"
        },
        {
          "line": 3455,
          "pattern": "leader_score",
          "text": "\"source_head\": \"def run_leader_engine_validation(\\n    symbols: list[str],\\n    prices_map: dict[str, list[float]],\\n    spx_prices: list[float],\\n    forward_days: list[int] = [5, 10, 20, 30],\\n    step: int = 5,           # 每隔 step 天计算一次（节省时间）\\n    min_history: int = 120,  # 最少需要多少天历史\\n) -> dict:\\"
        },
        {
          "line": 4067,
          "pattern": "E1R_UPTREND_CONFIRMED",
          "text": "\"value\": \"0 if _etype == 'E1R_UPTREND_CONFIRMED' else 1\""
        },
        {
          "line": 4067,
          "pattern": "UPTREND_CONFIRMED",
          "text": "\"value\": \"0 if _etype == 'E1R_UPTREND_CONFIRMED' else 1\""
        },
        {
          "line": 4107,
          "pattern": "E1R_UPTREND_CONFIRMED",
          "text": "\"value\": \"'E1R_UPTREND_CONFIRMED' if confirmed else 'E1R_UPTREND_EMERGING'\""
        },
        {
          "line": 4107,
          "pattern": "UPTREND_CONFIRMED",
          "text": "\"value\": \"'E1R_UPTREND_CONFIRMED' if confirmed else 'E1R_UPTREND_EMERGING'\""
        },
        {
          "line": 4117,
          "pattern": "E1R_UPTREND_CONFIRMED",
          "text": "\"value\": \"{'sym': _sym, 'sig': _sig, 'entry_type': _etype, 'target_size_units': 1.0 if _etype == 'E1R_UPTREND_CONFIRMED' else 0.5}\""
        },
        {
          "line": 4117,
          "pattern": "UPTREND_CONFIRMED",
          "text": "\"value\": \"{'sym': _sym, 'sig': _sig, 'entry_type': _etype, 'target_size_units': 1.0 if _etype == 'E1R_UPTREND_CONFIRMED' else 0.5}\""
        },
        {
          "line": 5412,
          "pattern": "E1R_UPTREND_CONFIRMED",
          "text": "\"text\": \"                    entry_type = \\\"E1R_UPTREND_CONFIRMED\\\" if confirmed else \\\"E1R_UPTREND_EMERGING\\\"\""
        },
        {
          "line": 5412,
          "pattern": "UPTREND_CONFIRMED",
          "text": "\"text\": \"                    entry_type = \\\"E1R_UPTREND_CONFIRMED\\\" if confirmed else \\\"E1R_UPTREND_EMERGING\\\"\""
        },
        {
          "line": 5463,
          "pattern": "E1R_UPTREND_CONFIRMED",
          "text": "\"text\": \"                _priority = 0 if _etype == \\\"E1R_UPTREND_CONFIRMED\\\" else 1\""
        },
        {
          "line": 5463,
          "pattern": "UPTREND_CONFIRMED",
          "text": "\"text\": \"                _priority = 0 if _etype == \\\"E1R_UPTREND_CONFIRMED\\\" else 1\""
        },
        {
          "line": 5498,
          "pattern": "E1R_UPTREND_CONFIRMED",
          "text": "\"text\": \"                        \\\"target_size_units\\\": 1.0 if _etype == \\\"E1R_UPTREND_CONFIRMED\\\" else 0.5,\""
        }
      ]
    },
    {
      "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0_E1_E1R_CORE_CONTRACT_AUDIT.json",
      "score": 195,
      "hits": [
        {
          "line": 2980,
          "pattern": "leader_score",
          "text": "\"text\": \"                    if reduce_primary == \\\"leader_score_below_60\\\":\""
        },
        {
          "line": 3075,
          "pattern": "leader_rank",
          "text": "\"text\": \"            leader_rank_all = {s: i + 1 for i, (s, _) in enumerate(top_ranked)}\""
        },
        {
          "line": 3101,
          "pattern": "E1R_UPTREND_CONFIRMED",
          "text": "\"text\": \"                    entry_type = \\\"E1R_UPTREND_CONFIRMED\\\" if confirmed else \\\"E1R_UPTREND_EMERGING\\\"\""
        },
        {
          "line": 3101,
          "pattern": "UPTREND_CONFIRMED",
          "text": "\"text\": \"                    entry_type = \\\"E1R_UPTREND_CONFIRMED\\\" if confirmed else \\\"E1R_UPTREND_EMERGING\\\"\""
        },
        {
          "line": 3219,
          "pattern": "E1R_UPTREND_CONFIRMED",
          "text": "\"text\": \"                _priority = 0 if _etype == \\\"E1R_UPTREND_CONFIRMED\\\" else 1\""
        },
        {
          "line": 3219,
          "pattern": "UPTREND_CONFIRMED",
          "text": "\"text\": \"                _priority = 0 if _etype == \\\"E1R_UPTREND_CONFIRMED\\\" else 1\""
        },
        {
          "line": 3249,
          "pattern": "E1R_UPTREND_CONFIRMED",
          "text": "\"text\": \"                        \\\"target_size_units\\\": 1.0 if _etype == \\\"E1R_UPTREND_CONFIRMED\\\" else 0.5,\""
        },
        {
          "line": 3249,
          "pattern": "UPTREND_CONFIRMED",
          "text": "\"text\": \"                        \\\"target_size_units\\\": 1.0 if _etype == \\\"E1R_UPTREND_CONFIRMED\\\" else 0.5,\""
        },
        {
          "line": 3304,
          "pattern": "leader_rank",
          "text": "\"text\": \"                    \\\"entry_rank\\\":     top_entry_rank.get(sym) or leader_rank_all.get(sym),\""
        },
        {
          "line": 3416,
          "pattern": "leader_score",
          "text": "\"text\": \"                        and reason_info.get(\\\"primary_reason\\\") == \\\"leader_score_below_60\\\"\""
        },
        {
          "line": 3539,
          "pattern": "leader_rank",
          "text": "\"text\": \"                    \\\"entry_rank\\\": top_entry_rank.get(sym) or leader_rank_all.get(sym),\""
        },
        {
          "line": 3551,
          "pattern": "momentum_acceleration",
          "text": "\"text\": \"                    \\\"reasons\\\": [\\\"emerging_upgraded_to_confirmed\\\", \\\"position_return_above_3pct\\\", \\\"close_above_ma20\\\", \\\"momentum_acceleration_non_negative\\\"],\""
        },
        {
          "line": 3569,
          "pattern": "momentum_acceleration",
          "text": "\"text\": \"                    \\\"reasons\\\": [\\\"emerging_upgraded_to_confirmed\\\", \\\"position_return_above_3pct\\\", \\\"close_above_ma20\\\", \\\"momentum_acceleration_non_negative\\\"],\""
        },
        {
          "line": 3573,
          "pattern": "E1R_UPTREND_CONFIRMED",
          "text": "\"text\": \"                    \\\"e1r_entry_type\\\": \\\"E1R_UPTREND_CONFIRMED\\\",\""
        },
        {
          "line": 3573,
          "pattern": "UPTREND_CONFIRMED",
          "text": "\"text\": \"                    \\\"e1r_entry_type\\\": \\\"E1R_UPTREND_CONFIRMED\\\",\""
        },
        {
          "line": 10648,
          "pattern": "leader_score",
          "text": "\"source\": \"def run_stateful_simulation(\\n    symbols:        list[str],\\n    prices_map:     dict[str, list[float]],\\n    dates_map:      dict[str, list[str]],\\n    spx_prices:     list[float],\\n    spx_dates:      list[str],\\n    ohlc_map:       dict = None,\\n    assumptions:    dict = None,\\n    s"
        }
      ]
    },
    {
      "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0_E1_E1R_CORE_CONTRACT_AUDIT.md",
      "score": 195,
      "hits": [
        {
          "line": 1833,
          "pattern": "leader_score",
          "text": "\"text\": \"                    if reduce_primary == \\\"leader_score_below_60\\\":\""
        },
        {
          "line": 1928,
          "pattern": "leader_rank",
          "text": "\"text\": \"            leader_rank_all = {s: i + 1 for i, (s, _) in enumerate(top_ranked)}\""
        },
        {
          "line": 1954,
          "pattern": "E1R_UPTREND_CONFIRMED",
          "text": "\"text\": \"                    entry_type = \\\"E1R_UPTREND_CONFIRMED\\\" if confirmed else \\\"E1R_UPTREND_EMERGING\\\"\""
        },
        {
          "line": 1954,
          "pattern": "UPTREND_CONFIRMED",
          "text": "\"text\": \"                    entry_type = \\\"E1R_UPTREND_CONFIRMED\\\" if confirmed else \\\"E1R_UPTREND_EMERGING\\\"\""
        },
        {
          "line": 2072,
          "pattern": "E1R_UPTREND_CONFIRMED",
          "text": "\"text\": \"                _priority = 0 if _etype == \\\"E1R_UPTREND_CONFIRMED\\\" else 1\""
        },
        {
          "line": 2072,
          "pattern": "UPTREND_CONFIRMED",
          "text": "\"text\": \"                _priority = 0 if _etype == \\\"E1R_UPTREND_CONFIRMED\\\" else 1\""
        },
        {
          "line": 2102,
          "pattern": "E1R_UPTREND_CONFIRMED",
          "text": "\"text\": \"                        \\\"target_size_units\\\": 1.0 if _etype == \\\"E1R_UPTREND_CONFIRMED\\\" else 0.5,\""
        },
        {
          "line": 2102,
          "pattern": "UPTREND_CONFIRMED",
          "text": "\"text\": \"                        \\\"target_size_units\\\": 1.0 if _etype == \\\"E1R_UPTREND_CONFIRMED\\\" else 0.5,\""
        },
        {
          "line": 2157,
          "pattern": "leader_rank",
          "text": "\"text\": \"                    \\\"entry_rank\\\":     top_entry_rank.get(sym) or leader_rank_all.get(sym),\""
        },
        {
          "line": 2269,
          "pattern": "leader_score",
          "text": "\"text\": \"                        and reason_info.get(\\\"primary_reason\\\") == \\\"leader_score_below_60\\\"\""
        }
      ]
    },
    {
      "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C2_RECOVER_5Y_PORTFOLIO_EQUITY_CANDIDATES.json",
      "score": 195,
      "hits": [
        {
          "line": 2337,
          "pattern": "leader_score",
          "text": "\"leader_score_entry\","
        },
        {
          "line": 2566,
          "pattern": "leader_score",
          "text": "\"leader_score_entry\","
        },
        {
          "line": 2830,
          "pattern": "leader_score",
          "text": "\"leader_score_entry\","
        },
        {
          "line": 3101,
          "pattern": "leader_score",
          "text": "\"leader_score_entry\","
        },
        {
          "line": 6823,
          "pattern": "leader_score",
          "text": "\"leader_score_entry\","
        },
        {
          "line": 7052,
          "pattern": "leader_score",
          "text": "\"leader_score_entry\","
        },
        {
          "line": 7316,
          "pattern": "leader_score",
          "text": "\"leader_score_entry\","
        },
        {
          "line": 7587,
          "pattern": "leader_score",
          "text": "\"leader_score_entry\","
        },
        {
          "line": 7834,
          "pattern": "leader_rank",
          "text": "\"leader_rank\","
        },
        {
          "line": 7835,
          "pattern": "leader_score",
          "text": "\"leader_score\","
        },
        {
          "line": 7973,
          "pattern": "leader_rank",
          "text": "\"leader_rank\","
        },
        {
          "line": 7974,
          "pattern": "leader_score",
          "text": "\"leader_score\","
        },
        {
          "line": 8112,
          "pattern": "leader_rank",
          "text": "\"leader_rank\","
        },
        {
          "line": 8113,
          "pattern": "leader_score",
          "text": "\"leader_score\","
        },
        {
          "line": 8251,
          "pattern": "leader_rank",
          "text": "\"leader_rank\","
        },
        {
          "line": 8252,
          "pattern": "leader_score",
          "text": "\"leader_score\","
        },
        {
          "line": 8390,
          "pattern": "leader_rank",
          "text": "\"leader_rank\","
        },
        {
          "line": 8391,
          "pattern": "leader_score",
          "text": "\"leader_score\","
        },
        {
          "line": 8529,
          "pattern": "leader_rank",
          "text": "\"leader_rank\","
        },
        {
          "line": 8530,
          "pattern": "leader_score",
          "text": "\"leader_score\","
        }
      ]
    },
    {
      "path": "docs/research/stage3_2_backtest_snapshots/backtest_feature_source_stage3_2.py",
      "score": 195,
      "hits": [
        {
          "line": 21,
          "pattern": "momentum_acceleration",
          "text": "momentum_score as calc_momentum, moving_average, linreg_slope, momentum_acceleration"
        },
        {
          "line": 24,
          "pattern": "leader_rank",
          "text": "from ..engine.leader_ranking import leader_score as calc_leader_score"
        },
        {
          "line": 24,
          "pattern": "leader_score",
          "text": "from ..engine.leader_ranking import leader_score as calc_leader_score"
        },
        {
          "line": 124,
          "pattern": "leader_score",
          "text": "def _rebuild_leader_score(prices: list[float], spx_prices: list[float],"
        },
        {
          "line": 153,
          "pattern": "leader_score",
          "text": "ls = calc_leader_score(rs, mom, th)"
        },
        {
          "line": 164,
          "pattern": "leader_score",
          "text": "\"leader_score\": ls,"
        },
        {
          "line": 209,
          "pattern": "leader_score",
          "text": "info = _rebuild_leader_score("
        },
        {
          "line": 222,
          "pattern": "leader_score",
          "text": "ls = info[\"leader_score\"]"
        },
        {
          "line": 375,
          "pattern": "leader_score",
          "text": "ls = calc_leader_score(rs, mom, th)"
        },
        {
          "line": 519,
          "pattern": "leader_score",
          "text": "ls = calc_leader_score(rs, mom, th)"
        },
        {
          "line": 522,
          "pattern": "leader_score",
          "text": "day_scores[sym] = {\"leader_score\": ls, \"promotion_score\": promo_approx}"
        },
        {
          "line": 528,
          "pattern": "leader_score",
          "text": "top30_now = set(sorted(day_scores, key=lambda s: day_scores[s][\"leader_score\"], reverse=True)[:30])"
        },
        {
          "line": 553,
          "pattern": "leader_score",
          "text": "future_scores[s] = calc_leader_score(frs, fmom, fth)"
        },
        {
          "line": 660,
          "pattern": "leader_score",
          "text": "ls    = calc_leader_score(rs, mom, th)"
        },
        {
          "line": 1177,
          "pattern": "leader_score",
          "text": "\"leader_score_entry\":    ls,"
        },
        {
          "line": 1289,
          "pattern": "leader_score",
          "text": "\"leader_score_entry\":   round(h.get(\"leader_score_entry\", 0), 1),"
        },
        {
          "line": 1337,
          "pattern": "leader_score",
          "text": "if reduce_primary == \"leader_score_below_60\":"
        },
        {
          "line": 1565,
          "pattern": "leader_score",
          "text": "ls      = calc_leader_score(rs, mom, th)"
        },
        {
          "line": 1576,
          "pattern": "rs_20d_improvement",
          "text": "rs_20d_improvement = 0.0"
        },
        {
          "line": 1580,
          "pattern": "rs_20d_improvement",
          "text": "rs_20d_improvement = round(rs - rs_prev20, 2)"
        }
      ]
    },
    {
      "path": "src/engine/backtest.py",
      "score": 195,
      "hits": [
        {
          "line": 21,
          "pattern": "momentum_acceleration",
          "text": "momentum_score as calc_momentum, moving_average, linreg_slope, momentum_acceleration"
        },
        {
          "line": 24,
          "pattern": "leader_rank",
          "text": "from ..engine.leader_ranking import leader_score as calc_leader_score"
        },
        {
          "line": 24,
          "pattern": "leader_score",
          "text": "from ..engine.leader_ranking import leader_score as calc_leader_score"
        },
        {
          "line": 124,
          "pattern": "leader_score",
          "text": "def _rebuild_leader_score(prices: list[float], spx_prices: list[float],"
        },
        {
          "line": 153,
          "pattern": "leader_score",
          "text": "ls = calc_leader_score(rs, mom, th)"
        },
        {
          "line": 164,
          "pattern": "leader_score",
          "text": "\"leader_score\": ls,"
        },
        {
          "line": 209,
          "pattern": "leader_score",
          "text": "info = _rebuild_leader_score("
        },
        {
          "line": 222,
          "pattern": "leader_score",
          "text": "ls = info[\"leader_score\"]"
        },
        {
          "line": 375,
          "pattern": "leader_score",
          "text": "ls = calc_leader_score(rs, mom, th)"
        },
        {
          "line": 519,
          "pattern": "leader_score",
          "text": "ls = calc_leader_score(rs, mom, th)"
        },
        {
          "line": 522,
          "pattern": "leader_score",
          "text": "day_scores[sym] = {\"leader_score\": ls, \"promotion_score\": promo_approx}"
        },
        {
          "line": 528,
          "pattern": "leader_score",
          "text": "top30_now = set(sorted(day_scores, key=lambda s: day_scores[s][\"leader_score\"], reverse=True)[:30])"
        },
        {
          "line": 553,
          "pattern": "leader_score",
          "text": "future_scores[s] = calc_leader_score(frs, fmom, fth)"
        },
        {
          "line": 660,
          "pattern": "leader_score",
          "text": "ls    = calc_leader_score(rs, mom, th)"
        },
        {
          "line": 1177,
          "pattern": "leader_score",
          "text": "\"leader_score_entry\":    ls,"
        },
        {
          "line": 1289,
          "pattern": "leader_score",
          "text": "\"leader_score_entry\":   round(h.get(\"leader_score_entry\", 0), 1),"
        },
        {
          "line": 1337,
          "pattern": "leader_score",
          "text": "if reduce_primary == \"leader_score_below_60\":"
        },
        {
          "line": 1565,
          "pattern": "leader_score",
          "text": "ls      = calc_leader_score(rs, mom, th)"
        },
        {
          "line": 1576,
          "pattern": "rs_20d_improvement",
          "text": "rs_20d_improvement = 0.0"
        },
        {
          "line": 1580,
          "pattern": "rs_20d_improvement",
          "text": "rs_20d_improvement = round(rs - rs_prev20, 2)"
        }
      ]
    },
    {
      "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C3FD_MARKET_STATE_GENERATOR_AUDIT.json",
      "score": 190,
      "hits": [
        {
          "line": 5158,
          "pattern": "rs_20d_improvement",
          "text": "\"text\": \"                rs_20d_improvement = round(rs - rs_prev20, 2)\""
        },
        {
          "line": 5162,
          "pattern": "momentum_acceleration",
          "text": "\"text\": \"            mom_acc = momentum_acceleration(p) if e1r_shell_mode else 0.0\""
        },
        {
          "line": 8642,
          "pattern": "leader_score",
          "text": "\"text\": \"                     \\\"leader_score\\\": s.get(\\\"leader_score\\\", 0),\""
        },
        {
          "line": 11931,
          "pattern": "E1R_UPTREND_CONFIRMED",
          "text": "\"text\": \"                    entry_type = \\\"E1R_UPTREND_CONFIRMED\\\" if confirmed else \\\"E1R_UPTREND_EMERGING\\\"\""
        },
        {
          "line": 11931,
          "pattern": "UPTREND_CONFIRMED",
          "text": "\"text\": \"                    entry_type = \\\"E1R_UPTREND_CONFIRMED\\\" if confirmed else \\\"E1R_UPTREND_EMERGING\\\"\""
        },
        {
          "line": 11965,
          "pattern": "E1R_UPTREND_CONFIRMED",
          "text": "\"text\": \"                _priority = 0 if _etype == \\\"E1R_UPTREND_CONFIRMED\\\" else 1\""
        },
        {
          "line": 11965,
          "pattern": "UPTREND_CONFIRMED",
          "text": "\"text\": \"                _priority = 0 if _etype == \\\"E1R_UPTREND_CONFIRMED\\\" else 1\""
        },
        {
          "line": 11973,
          "pattern": "E1R_UPTREND_CONFIRMED",
          "text": "\"text\": \"                        \\\"target_size_units\\\": 1.0 if _etype == \\\"E1R_UPTREND_CONFIRMED\\\" else 0.5,\""
        },
        {
          "line": 11973,
          "pattern": "UPTREND_CONFIRMED",
          "text": "\"text\": \"                        \\\"target_size_units\\\": 1.0 if _etype == \\\"E1R_UPTREND_CONFIRMED\\\" else 0.5,\""
        },
        {
          "line": 12046,
          "pattern": "E1R_UPTREND_CONFIRMED",
          "text": "\"text\": \"                    \\\"e1r_entry_type\\\": \\\"E1R_UPTREND_CONFIRMED\\\",\""
        },
        {
          "line": 12046,
          "pattern": "UPTREND_CONFIRMED",
          "text": "\"text\": \"                    \\\"e1r_entry_type\\\": \\\"E1R_UPTREND_CONFIRMED\\\",\""
        }
      ]
    },
    {
      "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2A_ENGINE_ENTRYPOINT_REPORT.json",
      "score": 175,
      "hits": [
        {
          "line": 365,
          "pattern": "leader_score",
          "text": "\"body_head\": \"def run_leader_engine_validation(\\n    symbols: list[str],\\n    prices_map: dict[str, list[float]],\\n    spx_prices: list[float],\\n    forward_days: list[int] = [5, 10, 20, 30],\\n    step: int = 5,           # 每隔 step 天计算一次（节省时间）\\n    min_history: int = 120,  # 最少需要多少天历史\\n) -> dict:\\n "
        },
        {
          "line": 382,
          "pattern": "leader_score",
          "text": "\"body_head\": \"def run_trade_rule_validation(\\n    symbols: list[str],\\n    prices_map: dict[str, list[float]],\\n    spx_prices: list[float],\\n    forward_days: list[int] = [5, 10, 20, 30],\\n    step: int = 5,\\n    min_history: int = 120,\\n    market_score_default: float = 60.0,\\n) -> dict:\\n    \\\"\\\""
        },
        {
          "line": 399,
          "pattern": "leader_score",
          "text": "\"body_head\": \"def run_promotion_engine_validation(\\n    symbols: list[str],\\n    prices_map: dict[str, list[float]],\\n    spx_prices: list[float],\\n    promotion_thresholds: list[int] = [80, 85, 90],\\n    track_days: list[int] = [5, 10, 20, 30],\\n    step: int = 5,\\n    min_history: int = 120,\\n) ->"
        },
        {
          "line": 418,
          "pattern": "leader_score",
          "text": "\"body_head\": \"def run_action_forward_validation(\\n    symbols:       list[str],\\n    prices_map:    dict[str, list[float]],\\n    spx_prices:    list[float],\\n    dates_map:     dict[str, list[str]] | None = None,\\n    spx_dates:     list[str] | None = None,\\n    forward_days:  list[int] = [5, 10, 20"
        },
        {
          "line": 655,
          "pattern": "leader_score",
          "text": "\"body_head\": \"def run_leader_engine_validation(\\n    symbols: list[str],\\n    prices_map: dict[str, list[float]],\\n    spx_prices: list[float],\\n    forward_days: list[int] = [5, 10, 20, 30],\\n    step: int = 5,           # 每隔 step 天计算一次（节省时间）\\n    min_history: int = 120,  # 最少需要多少天历史\\n) -> dict:\\n "
        },
        {
          "line": 672,
          "pattern": "leader_score",
          "text": "\"body_head\": \"def run_trade_rule_validation(\\n    symbols: list[str],\\n    prices_map: dict[str, list[float]],\\n    spx_prices: list[float],\\n    forward_days: list[int] = [5, 10, 20, 30],\\n    step: int = 5,\\n    min_history: int = 120,\\n    market_score_default: float = 60.0,\\n) -> dict:\\n    \\\"\\\""
        },
        {
          "line": 689,
          "pattern": "leader_score",
          "text": "\"body_head\": \"def run_promotion_engine_validation(\\n    symbols: list[str],\\n    prices_map: dict[str, list[float]],\\n    spx_prices: list[float],\\n    promotion_thresholds: list[int] = [80, 85, 90],\\n    track_days: list[int] = [5, 10, 20, 30],\\n    step: int = 5,\\n    min_history: int = 120,\\n) ->"
        },
        {
          "line": 708,
          "pattern": "leader_score",
          "text": "\"body_head\": \"def run_action_forward_validation(\\n    symbols:       list[str],\\n    prices_map:    dict[str, list[float]],\\n    spx_prices:    list[float],\\n    dates_map:     dict[str, list[str]] | None = None,\\n    spx_dates:     list[str] | None = None,\\n    forward_days:  list[int] = [5, 10, 20"
        },
        {
          "line": 785,
          "pattern": "momentum_acceleration",
          "text": "\"momentum_acceleration\""
        },
        {
          "line": 797,
          "pattern": "leader_rank",
          "text": "\"module\": \"engine.leader_ranking\","
        },
        {
          "line": 799,
          "pattern": "leader_score",
          "text": "\"leader_score\""
        },
        {
          "line": 3010,
          "pattern": "leader_rank",
          "text": "\"text\": \"            leader_rank_all = {s: i + 1 for i, (s, _) in enumerate(top_ranked)}\""
        },
        {
          "line": 3018,
          "pattern": "leader_rank",
          "text": "\"text\": \"                rank_all = leader_rank_all.get(sym, 9999)\""
        },
        {
          "line": 3062,
          "pattern": "leader_rank",
          "text": "\"text\": \"                        \\\"leader_rank\\\": rank_all,\""
        },
        {
          "line": 15735,
          "pattern": "leader_rank",
          "text": "\"module\": \"engine.leader_ranking\","
        },
        {
          "line": 16256,
          "pattern": "leader_rank",
          "text": "\"src/engine/leader_ranking.py\": {"
        },
        {
          "line": 16257,
          "pattern": "leader_rank",
          "text": "\"path\": \"src/engine/leader_ranking.py\","
        },
        {
          "line": 16292,
          "pattern": "momentum_acceleration",
          "text": "\"compute_momentum_acceleration\","
        },
        {
          "line": 16335,
          "pattern": "momentum_acceleration",
          "text": "\"momentum_acceleration\","
        },
        {
          "line": 16354,
          "pattern": "leader_rank",
          "text": "\"module\": \"engine.leader_ranking\","
        }
      ]
    }
  ],
  "uptrend_emerging": [
    {
      "path": "scripts/audit_e1r_original_contract_4c2c4a.py",
      "score": 225,
      "hits": [
        {
          "line": 55,
          "pattern": "emerging",
          "text": "\"uptrend_emerging\": ["
        },
        {
          "line": 56,
          "pattern": "E1R_UPTREND_EMERGING",
          "text": "\"E1R_UPTREND_EMERGING\","
        },
        {
          "line": 57,
          "pattern": "Emerging",
          "text": "\"Emerging\","
        },
        {
          "line": 58,
          "pattern": "diagnostic_only",
          "text": "\"diagnostic_only\","
        },
        {
          "line": 59,
          "pattern": "emerging",
          "text": "\"emerging\","
        },
        {
          "line": 340,
          "pattern": "emerging",
          "text": "\"evidence_groups\": [\"uptrend_confirmed\", \"uptrend_emerging\", \"position_cap\"],"
        }
      ]
    },
    {
      "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C1_PREFLIGHT_REPORT.json",
      "score": 195,
      "hits": [
        {
          "line": 70,
          "pattern": "diagnostic_only",
          "text": "\"no_diagnostic_only_rows\": true,"
        },
        {
          "line": 2346,
          "pattern": "emerging",
          "text": "\"text\": \"                if emerging or confirmed:\""
        },
        {
          "line": 2350,
          "pattern": "E1R_UPTREND_EMERGING",
          "text": "\"text\": \"                    entry_type = \\\"E1R_UPTREND_CONFIRMED\\\" if confirmed else \\\"E1R_UPTREND_EMERGING\\\"\""
        },
        {
          "line": 2354,
          "pattern": "emerging",
          "text": "\"text\": \"                    reasons = confirmed_reasons if confirmed else emerging_reasons\""
        },
        {
          "line": 2362,
          "pattern": "emerging",
          "text": "\"text\": \"                    sig[\\\"e1r_uptrend_emerging_eligible\\\"] = emerging\""
        },
        {
          "line": 2395,
          "pattern": "emerging",
          "text": "\"text\": \"                        \\\"e1r_uptrend_emerging_eligible\\\": emerging,\""
        },
        {
          "line": 2411,
          "pattern": "diagnostic_only",
          "text": "\"text\": \"                        \\\"diagnostic_only\\\": True,\""
        },
        {
          "line": 2591,
          "pattern": "Emerging",
          "text": "\"text\": \"        # E1-R Phase 3B: Emerging → Confirmed upgrade ADD.\""
        },
        {
          "line": 2639,
          "pattern": "E1R_UPTREND_EMERGING",
          "text": "\"text\": \"                if h.get(\\\"e1r_entry_type\\\") != \\\"E1R_UPTREND_EMERGING\\\":\""
        },
        {
          "line": 2679,
          "pattern": "emerging",
          "text": "\"text\": \"                    \\\"primary_reason\\\": \\\"emerging_upgraded_to_confirmed\\\",\""
        },
        {
          "line": 2683,
          "pattern": "emerging",
          "text": "\"text\": \"                    \\\"reasons\\\": [\\\"emerging_upgraded_to_confirmed\\\", \\\"position_return_above_3pct\\\", \\\"close_above_ma20\\\", \\\"momentum_acceleration_non_negative\\\"],\""
        },
        {
          "line": 2703,
          "pattern": "emerging",
          "text": "\"text\": \"                    \\\"primary_reason\\\": \\\"emerging_upgraded_to_confirmed\\\",\""
        },
        {
          "line": 2707,
          "pattern": "emerging",
          "text": "\"text\": \"                    \\\"reasons\\\": [\\\"emerging_upgraded_to_confirmed\\\", \\\"position_return_above_3pct\\\", \\\"close_above_ma20\\\", \\\"momentum_acceleration_non_negative\\\"],\""
        },
        {
          "line": 2723,
          "pattern": "emerging",
          "text": "\"text\": \"                skip_reasons[\\\"e1r_emerging_to_confirmed_add\\\"] += 1\""
        }
      ]
    },
    {
      "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10A_DIRECT_GENERATOR_FUNCTION_AUDIT.json",
      "score": 195,
      "hits": [
        {
          "line": 4107,
          "pattern": "E1R_UPTREND_EMERGING",
          "text": "\"value\": \"'E1R_UPTREND_CONFIRMED' if confirmed else 'E1R_UPTREND_EMERGING'\""
        },
        {
          "line": 5412,
          "pattern": "E1R_UPTREND_EMERGING",
          "text": "\"text\": \"                    entry_type = \\\"E1R_UPTREND_CONFIRMED\\\" if confirmed else \\\"E1R_UPTREND_EMERGING\\\"\""
        },
        {
          "line": 5702,
          "pattern": "E1R_UPTREND_EMERGING",
          "text": "\"text\": \"                if h.get(\\\"e1r_entry_type\\\") != \\\"E1R_UPTREND_EMERGING\\\":\""
        }
      ]
    },
    {
      "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0_E1_E1R_CORE_CONTRACT_AUDIT.json",
      "score": 195,
      "hits": [
        {
          "line": 3097,
          "pattern": "emerging",
          "text": "\"text\": \"                if emerging or confirmed:\""
        },
        {
          "line": 3101,
          "pattern": "E1R_UPTREND_EMERGING",
          "text": "\"text\": \"                    entry_type = \\\"E1R_UPTREND_CONFIRMED\\\" if confirmed else \\\"E1R_UPTREND_EMERGING\\\"\""
        },
        {
          "line": 3105,
          "pattern": "emerging",
          "text": "\"text\": \"                    reasons = confirmed_reasons if confirmed else emerging_reasons\""
        },
        {
          "line": 3138,
          "pattern": "emerging",
          "text": "\"text\": \"                        \\\"e1r_uptrend_emerging_eligible\\\": emerging,\""
        },
        {
          "line": 3513,
          "pattern": "E1R_UPTREND_EMERGING",
          "text": "\"text\": \"                if h.get(\\\"e1r_entry_type\\\") != \\\"E1R_UPTREND_EMERGING\\\":\""
        },
        {
          "line": 3547,
          "pattern": "emerging",
          "text": "\"text\": \"                    \\\"primary_reason\\\": \\\"emerging_upgraded_to_confirmed\\\",\""
        },
        {
          "line": 3551,
          "pattern": "emerging",
          "text": "\"text\": \"                    \\\"reasons\\\": [\\\"emerging_upgraded_to_confirmed\\\", \\\"position_return_above_3pct\\\", \\\"close_above_ma20\\\", \\\"momentum_acceleration_non_negative\\\"],\""
        },
        {
          "line": 3565,
          "pattern": "emerging",
          "text": "\"text\": \"                    \\\"primary_reason\\\": \\\"emerging_upgraded_to_confirmed\\\",\""
        },
        {
          "line": 3569,
          "pattern": "emerging",
          "text": "\"text\": \"                    \\\"reasons\\\": [\\\"emerging_upgraded_to_confirmed\\\", \\\"position_return_above_3pct\\\", \\\"close_above_ma20\\\", \\\"momentum_acceleration_non_negative\\\"],\""
        },
        {
          "line": 10648,
          "pattern": "emerging",
          "text": "\"source\": \"def run_stateful_simulation(\\n    symbols:        list[str],\\n    prices_map:     dict[str, list[float]],\\n    dates_map:      dict[str, list[str]],\\n    spx_prices:     list[float],\\n    spx_dates:      list[str],\\n    ohlc_map:       dict = None,\\n    assumptions:    dict = None,\\n    s"
        }
      ]
    },
    {
      "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0_E1_E1R_CORE_CONTRACT_AUDIT.md",
      "score": 195,
      "hits": [
        {
          "line": 1950,
          "pattern": "emerging",
          "text": "\"text\": \"                if emerging or confirmed:\""
        },
        {
          "line": 1954,
          "pattern": "E1R_UPTREND_EMERGING",
          "text": "\"text\": \"                    entry_type = \\\"E1R_UPTREND_CONFIRMED\\\" if confirmed else \\\"E1R_UPTREND_EMERGING\\\"\""
        },
        {
          "line": 1958,
          "pattern": "emerging",
          "text": "\"text\": \"                    reasons = confirmed_reasons if confirmed else emerging_reasons\""
        },
        {
          "line": 1991,
          "pattern": "emerging",
          "text": "\"text\": \"                        \\\"e1r_uptrend_emerging_eligible\\\": emerging,\""
        }
      ]
    },
    {
      "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C2_RECOVER_5Y_PORTFOLIO_EQUITY_CANDIDATES.json",
      "score": 195,
      "hits": [
        {
          "line": 8940,
          "pattern": "diagnostic_only",
          "text": "\"diagnostic_only\","
        },
        {
          "line": 8943,
          "pattern": "emerging",
          "text": "\"e1r_uptrend_emerging_eligible\","
        },
        {
          "line": 9004,
          "pattern": "diagnostic_only",
          "text": "\"diagnostic_only\","
        },
        {
          "line": 9007,
          "pattern": "emerging",
          "text": "\"e1r_uptrend_emerging_eligible\","
        },
        {
          "line": 18281,
          "pattern": "diagnostic_only",
          "text": "\"diagnostic_only\","
        },
        {
          "line": 18284,
          "pattern": "emerging",
          "text": "\"e1r_uptrend_emerging_eligible\","
        },
        {
          "line": 18345,
          "pattern": "diagnostic_only",
          "text": "\"diagnostic_only\","
        },
        {
          "line": 18348,
          "pattern": "emerging",
          "text": "\"e1r_uptrend_emerging_eligible\","
        },
        {
          "line": 20016,
          "pattern": "E1R_UPTREND_EMERGING",
          "text": "\"text\": \"                    entry_type = \\\"E1R_UPTREND_CONFIRMED\\\" if confirmed else \\\"E1R_UPTREND_EMERGING\\\"\""
        },
        {
          "line": 20080,
          "pattern": "E1R_UPTREND_EMERGING",
          "text": "\"text\": \"                if h.get(\\\"e1r_entry_type\\\") != \\\"E1R_UPTREND_EMERGING\\\":\""
        },
        {
          "line": 22082,
          "pattern": "E1R_UPTREND_EMERGING",
          "text": "\"text\": \"          \\\"first_row_preview\\\": \\\"{\\\\n  \\\\\\\"date\\\\\\\": \\\\\\\"2021-06-11\\\\\\\",\\\\n  \\\\\\\"symbol\\\\\\\": \\\\\\\"ADBE\\\\\\\",\\\\n  \\\\\\\"spx_regime\\\\\\\": \\\\\\\"UPTREND\\\\\\\",\\\\n  \\\\\\\"e1r_entry_type\\\\\\\": \\\\\\\"E1R_UPTREND_EMERGING\\\\\\\",\\\\n  \\\\\\\"e1r_uptrend_emerging_eligible\\\\\\\": true,\\\\n  \\\\\\\"e1r_uptrend_confirmed_elig"
        },
        {
          "line": 22082,
          "pattern": "emerging",
          "text": "\"text\": \"          \\\"first_row_preview\\\": \\\"{\\\\n  \\\\\\\"date\\\\\\\": \\\\\\\"2021-06-11\\\\\\\",\\\\n  \\\\\\\"symbol\\\\\\\": \\\\\\\"ADBE\\\\\\\",\\\\n  \\\\\\\"spx_regime\\\\\\\": \\\\\\\"UPTREND\\\\\\\",\\\\n  \\\\\\\"e1r_entry_type\\\\\\\": \\\\\\\"E1R_UPTREND_EMERGING\\\\\\\",\\\\n  \\\\\\\"e1r_uptrend_emerging_eligible\\\\\\\": true,\\\\n  \\\\\\\"e1r_uptrend_confirmed_elig"
        },
        {
          "line": 22091,
          "pattern": "E1R_UPTREND_EMERGING",
          "text": "\"text\": \"          \\\"last_row_preview\\\": \\\"{\\\\n  \\\\\\\"date\\\\\\\": \\\\\\\"2026-06-16\\\\\\\",\\\\n  \\\\\\\"symbol\\\\\\\": \\\\\\\"WSM\\\\\\\",\\\\n  \\\\\\\"spx_regime\\\\\\\": \\\\\\\"UPTREND\\\\\\\",\\\\n  \\\\\\\"e1r_entry_type\\\\\\\": \\\\\\\"E1R_UPTREND_EMERGING\\\\\\\",\\\\n  \\\\\\\"e1r_uptrend_emerging_eligible\\\\\\\": true,\\\\n  \\\\\\\"e1r_uptrend_confirmed_eligib"
        },
        {
          "line": 22091,
          "pattern": "emerging",
          "text": "\"text\": \"          \\\"last_row_preview\\\": \\\"{\\\\n  \\\\\\\"date\\\\\\\": \\\\\\\"2026-06-16\\\\\\\",\\\\n  \\\\\\\"symbol\\\\\\\": \\\\\\\"WSM\\\\\\\",\\\\n  \\\\\\\"spx_regime\\\\\\\": \\\\\\\"UPTREND\\\\\\\",\\\\n  \\\\\\\"e1r_entry_type\\\\\\\": \\\\\\\"E1R_UPTREND_EMERGING\\\\\\\",\\\\n  \\\\\\\"e1r_uptrend_emerging_eligible\\\\\\\": true,\\\\n  \\\\\\\"e1r_uptrend_confirmed_eligib"
        },
        {
          "line": 22116,
          "pattern": "E1R_UPTREND_EMERGING",
          "text": "\"text\": \"          \\\"first_row_preview\\\": \\\"{\\\\n  \\\\\\\"date\\\\\\\": \\\\\\\"2021-06-11\\\\\\\",\\\\n  \\\\\\\"symbol\\\\\\\": \\\\\\\"ADBE\\\\\\\",\\\\n  \\\\\\\"spx_regime\\\\\\\": \\\\\\\"UPTREND\\\\\\\",\\\\n  \\\\\\\"e1r_entry_type\\\\\\\": \\\\\\\"E1R_UPTREND_EMERGING\\\\\\\",\\\\n  \\\\\\\"e1r_uptrend_emerging_eligible\\\\\\\": true,\\\\n  \\\\\\\"e1r_uptrend_confirmed_elig"
        },
        {
          "line": 22116,
          "pattern": "emerging",
          "text": "\"text\": \"          \\\"first_row_preview\\\": \\\"{\\\\n  \\\\\\\"date\\\\\\\": \\\\\\\"2021-06-11\\\\\\\",\\\\n  \\\\\\\"symbol\\\\\\\": \\\\\\\"ADBE\\\\\\\",\\\\n  \\\\\\\"spx_regime\\\\\\\": \\\\\\\"UPTREND\\\\\\\",\\\\n  \\\\\\\"e1r_entry_type\\\\\\\": \\\\\\\"E1R_UPTREND_EMERGING\\\\\\\",\\\\n  \\\\\\\"e1r_uptrend_emerging_eligible\\\\\\\": true,\\\\n  \\\\\\\"e1r_uptrend_confirmed_elig"
        },
        {
          "line": 22125,
          "pattern": "E1R_UPTREND_EMERGING",
          "text": "\"text\": \"          \\\"last_row_preview\\\": \\\"{\\\\n  \\\\\\\"date\\\\\\\": \\\\\\\"2026-06-16\\\\\\\",\\\\n  \\\\\\\"symbol\\\\\\\": \\\\\\\"WSM\\\\\\\",\\\\n  \\\\\\\"spx_regime\\\\\\\": \\\\\\\"UPTREND\\\\\\\",\\\\n  \\\\\\\"e1r_entry_type\\\\\\\": \\\\\\\"E1R_UPTREND_EMERGING\\\\\\\",\\\\n  \\\\\\\"e1r_uptrend_emerging_eligible\\\\\\\": true,\\\\n  \\\\\\\"e1r_uptrend_confirmed_eligib"
        },
        {
          "line": 22125,
          "pattern": "emerging",
          "text": "\"text\": \"          \\\"last_row_preview\\\": \\\"{\\\\n  \\\\\\\"date\\\\\\\": \\\\\\\"2026-06-16\\\\\\\",\\\\n  \\\\\\\"symbol\\\\\\\": \\\\\\\"WSM\\\\\\\",\\\\n  \\\\\\\"spx_regime\\\\\\\": \\\\\\\"UPTREND\\\\\\\",\\\\n  \\\\\\\"e1r_entry_type\\\\\\\": \\\\\\\"E1R_UPTREND_EMERGING\\\\\\\",\\\\n  \\\\\\\"e1r_uptrend_emerging_eligible\\\\\\\": true,\\\\n  \\\\\\\"e1r_uptrend_confirmed_eligib"
        },
        {
          "line": 22142,
          "pattern": "E1R_UPTREND_EMERGING",
          "text": "\"text\": \"          \\\"first_row_preview\\\": \\\"{\\\\n  \\\\\\\"date\\\\\\\": \\\\\\\"2021-06-11\\\\\\\",\\\\n  \\\\\\\"symbol\\\\\\\": \\\\\\\"ADBE\\\\\\\",\\\\n  \\\\\\\"spx_regime\\\\\\\": \\\\\\\"UPTREND\\\\\\\",\\\\n  \\\\\\\"e1r_entry_type\\\\\\\": \\\\\\\"E1R_UPTREND_EMERGING\\\\\\\",\\\\n  \\\\\\\"e1r_uptrend_emerging_eligible\\\\\\\": true,\\\\n  \\\\\\\"e1r_uptrend_confirmed_elig"
        },
        {
          "line": 22142,
          "pattern": "emerging",
          "text": "\"text\": \"          \\\"first_row_preview\\\": \\\"{\\\\n  \\\\\\\"date\\\\\\\": \\\\\\\"2021-06-11\\\\\\\",\\\\n  \\\\\\\"symbol\\\\\\\": \\\\\\\"ADBE\\\\\\\",\\\\n  \\\\\\\"spx_regime\\\\\\\": \\\\\\\"UPTREND\\\\\\\",\\\\n  \\\\\\\"e1r_entry_type\\\\\\\": \\\\\\\"E1R_UPTREND_EMERGING\\\\\\\",\\\\n  \\\\\\\"e1r_uptrend_emerging_eligible\\\\\\\": true,\\\\n  \\\\\\\"e1r_uptrend_confirmed_elig"
        }
      ]
    },
    {
      "path": "docs/research/stage3_2_backtest_snapshots/backtest_feature_source_stage3_2.py",
      "score": 195,
      "hits": [
        {
          "line": 1051,
          "pattern": "emerging",
          "text": "\"e1r_emerging_to_confirmed_add\":   0,   # E1-R execution: upgrade ADD generated"
        },
        {
          "line": 1544,
          "pattern": "Emerging",
          "text": "# E1-R Phase 3A: previous RS reference for Emerging Leader acceleration."
        },
        {
          "line": 1608,
          "pattern": "emerging",
          "text": "\"e1r_uptrend_emerging_eligible\": False,"
        },
        {
          "line": 1627,
          "pattern": "emerging",
          "text": "emerging_reasons = []"
        },
        {
          "line": 1628,
          "pattern": "emerging",
          "text": "if sig[\"rs_score\"] >= 80: emerging_reasons.append(\"rs_above_80\")"
        },
        {
          "line": 1629,
          "pattern": "emerging",
          "text": "if sig.get(\"rs_20d_improvement\", 0) >= 10: emerging_reasons.append(\"rs_20d_improvement_above_10\")"
        },
        {
          "line": 1630,
          "pattern": "emerging",
          "text": "if sig[\"momentum_score\"] >= 70: emerging_reasons.append(\"momentum_above_70\")"
        },
        {
          "line": 1631,
          "pattern": "emerging",
          "text": "if sig.get(\"momentum_acceleration\", 0) > 0: emerging_reasons.append(\"mom
```

## Artifact Summary

```json
[
  {
    "path": "exports/e1r_unified_5y_full_account_v1_result.json",
    "exists": true,
    "json_ok": true,
    "top_keys": [
      "alpha_pct",
      "avg_execution_drag_pct",
      "avg_holding_days",
      "avg_loser_pct",
      "avg_winner_pct",
      "cagr_pct",
      "daily_equity_record_count",
      "daily_equity_records",
      "daily_records",
      "e1r_candidate_count",
      "e1r_candidates",
      "e1r_uptrend_execution_enabled",
      "entry_top_n",
      "equity_curve",
      "executed_exit_reason_distribution",
      "executed_reduce_reason_distribution",
      "execution_model",
      "exposure_pct",
      "final_equity",
      "initial_capital",
      "invalid_trades",
      "invalid_trades_count",
      "layer",
      "market_entry_gate",
      "max_drawdown_pct",
      "name",
      "number_of_trades",
      "p0_passed",
      "partial_take_profit",
      "pending_orders_executed",
      "pending_orders_skipped",
      "pending_signal_reason_distribution",
      "portfolio_action_distribution",
      "profit_factor",
      "rank_based_exit",
      "sample_validity",
      "sharpe_ratio",
      "sim_end_liquidation_record",
      "skipped_orders_by_reason",
      "spx_cagr_pct",
      "spx_curve",
      "spx_total_return_pct",
      "status",
      "strategy_controls",
      "strategy_variant",
      "total_return_pct",
      "total_trades_all",
      "trades",
      "version",
      "win_rate_pct"
    ],
    "strategy_variant": "E1R_UNIFIED_5Y_FULL_ACCOUNT_V1",
    "version": "v1.6-top3-rs-minhold-relstop",
    "status": "INVALID",
    "total_return_pct": -100.0,
    "spx_total_return_pct": 76.84,
    "alpha_pct": -176.84,
    "final_equity": 0.16,
    "max_drawdown_pct": 100.0,
    "number_of_trades": 10,
    "total_trades_all": 10,
    "e1r_candidate_count": 8822,
    "strategy_controls_extract": {
      "candidate_top_n": 10,
      "entry_rs_min": 90.0,
      "min_holding_days": 10,
      "e1r_regime_wiring_enabled": true,
      "e1r_regime_source": "data/research/e1_5y/regimes/spx_regime_daily.json"
    }
  },
  {
    "path": "exports/e1r_unified_5y_full_account_v1_summary.json",
    "exists": true,
    "json_ok": true,
    "top_keys": [
      "artifact_type",
      "assumption_summary",
      "generated_at",
      "metrics",
      "record_summary",
      "simulation",
      "strategy_id",
      "trade_summary",
      "validations"
    ],
    "metrics_extract": {
      "total_return_pct": -100.0,
      "spx_total_return_pct": 76.84,
      "alpha_pct": -176.84,
      "cagr_pct": -93.05,
      "max_drawdown_pct": 100.0,
      "sharpe_ratio": 0,
      "final_equity": 0.16
    },
    "record_summary_extract": {
      "row_count": 1259,
      "date_start": "2021-06-11",
      "date_end": "2026-06-16",
      "regime_counts": {
        "UPTREND": 860,
        "SIDEWAYS": 241,
        "DOWNTREND": 158
      },
      "active_mode_counts": {
        "UPTREND_EMERGING_CONFIRMED_ENABLED": 860,
        "SIDEWAYS_QUALITY_BREAKOUT_ONLY": 241,
        "DOWNTREND_EXCEPTION_ONLY": 158
      },
      "risk_budget_mode_counts": {
        "UPTREND_RISK_ON": 860,
        "SIDEWAYS_LIMITED": 241,
        "DOWNTREND_DEFENSIVE": 158
      }
    }
  },
  {
    "path": "exports/e1r_unified_5y_dashboard_research_bundle.json",
    "exists": true,
    "json_ok": true,
    "top_keys": [
      "artifact_type",
      "curve",
      "display_scope",
      "do_not_use",
      "generated_at",
      "metric_source",
      "metrics",
      "regime_summary",
      "source_files",
      "status",
      "strategy_id",
      "validation",
      "warnings"
    ],
    "status": "DASHBOARD_RESEARCH_BUNDLE_READY_ACCOUNT_LEVEL_ONLY",
    "metrics_extract": {
      "total_return_pct": 65.71578,
      "spx_total_return_pct": 76.84,
      "alpha_pct": -11.124220000000008,
      "cagr_pct": 10.638841693504443,
      "max_drawdown_pct": 52.18893,
      "sharpe_ratio": 0.5017379738002563,
      "row_count": 1259,
      "final_equity": 165715.78
    },
    "curve_rows_count": 1259
  },
  {
    "path": "exports/e1r_unified_5y_full_account_v1_row_derived_summary.json",
    "exists": true,
    "json_ok": true,
    "top_keys": [
      "artifact_type",
      "engine_reported_metrics_rejected",
      "generated_at",
      "metric_consistency_diagnosis",
      "next_action",
      "row_derived_metrics",
      "sample_validity_from_engine",
      "source_metric_audit",
      "source_raw_summary",
      "source_result",
      "status",
      "strategy_id",
      "trade_layer_audit",
      "validation"
    ],
    "status": "ROW_DERIVED_ACCOUNT_METRICS_VALIDATED_TRADE_METRICS_NOT_VALIDATED",
    "row_derived_metrics_extract": {
      "total_return_pct": 65.71578,
      "spx_total_return_pct": 76.84,
      "alpha_pct": -11.124220000000008,
      "cagr_pct": 10.638841693504443,
      "max_drawdown_pct": 52.18893,
      "row_count": 1259,
      "final_exposure_pct": 100.0
    }
  },
  {
    "path": "exports/e1r_unified_5y_max3_contract_result.json",
    "exists": false,
    "json_ok": false
  },
  {
    "path": "exports/portfolio_backtest.json",
    "exists": true,
    "json_ok": true,
    "top_keys": [
      "alpha_pct",
      "avg_execution_drag_pct",
      "avg_holding_days",
      "avg_loser_pct",
      "avg_winner_pct",
      "cagr_pct",
      "comparison",
      "daily_records",
      "entry_top_n",
      "executed_exit_reason_distribution",
      "executed_reduce_reason_distribution",
      "execution_model",
      "exposure_pct",
      "final_equity",
      "generated_at",
      "generated_at_display",
      "initial_capital",
      "invalid_trades",
      "invalid_trades_count",
      "layer",
      "market_entry_gate",
      "max_drawdown_pct",
      "name",
      "number_of_trades",
      "p0_passed",
      "partial_take_profit",
      "pending_orders_executed",
      "pending_orders_skipped",
      "pending_signal_reason_distribution",
      "period_comparison",
      "portfolio_action_distribution",
      "profit_factor",
      "rank_based_exit",
      "sample_validity",
      "selected_variant",
      "selection_policy",
      "sharpe_ratio",
      "skipped_orders_by_reason",
      "spx_cagr_pct",
      "spx_total_return_pct",
      "status",
      "strategy_controls",
      "strategy_variant",
      "total_return_pct",
      "total_trades_all",
      "variant_results",
      "version",
      "win_rate_pct"
    ],
    "strategy_variant": "E1_audited_g4_minhold10",
    "version": "v1.6-ls60-mode-comparison",
    "status": "PARTIAL",
    "total_return_pct": 7.52,
    "spx_total_return_pct": 69.36,
    "alpha_pct": -61.84,
    "final_equity": 107519.31,
    "max_drawdown_pct": 38.1,
    "number_of_trades": 47,
    "total_trades_all": 47,
    "strategy_controls_extract": {
      "candidate_top_n": null,
      "entry_rs_min": 90.0,
      "min_holding_days": 10
    }
  },
  {
    "path": "exports/backtest.json",
    "exists": true,
    "json_ok": true,
    "top_keys": [
      "backtest",
      "generated_at",
      "generated_at_display"
    ]
  },
  {
    "path": "data/research/e1_5y/regimes/spx_regime_daily.json",
    "exists": true,
    "json_ok": true,
    "top_keys": [
      "daily_regime",
      "generated_at",
      "validation_window"
    ]
  }
]
```

## Conclusion

- `CONTRACT_SOURCES_LOCATED_FOR_REVIEW_BUT_EXECUTABLE_ENTRYPOINTS_NOT_YET_LOCKED`
- Recommended: Review the top source hits for UPTREND and SIDEWAYS/MA_CONFLICT, then create a no-strategy-change combined-run adapter that calls only the recovered original entrypoints and enforces global open_positions_count <= 3.

