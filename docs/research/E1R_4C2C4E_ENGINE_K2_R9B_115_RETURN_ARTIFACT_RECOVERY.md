# E1R 4C-2C-4E-ENGINE-K2-R9B — 115 Return Artifact Recovery

Generated At: `2026-07-11T02:11:48.500115+00:00`

## Purpose
Recover the generation chain and parameter evidence for exports/e1r_v0_2_backtest_summary.json without changing strategy logic.

## Target Artifact Inspection
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

## Evidence Status
```json
{
  "target_artifact_exists": true,
  "target_return_verified": true,
  "generator_script_candidates_found": true,
  "generator_script_candidates": [
    {
      "path": "scripts/e1r_k2_r9b_115_return_artifact_recovery.py",
      "score": 3460,
      "matched_terms": [
        "116.74",
        "116.7435999134756",
        "D3_RISK_OFF_PLUS_SHOCK_GATE",
        "E1R_REGIME_AWARE_V0_1",
        "E1R_REGIME_AWARE_V0_2",
        "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE",
        "e1r_composer",
        "e1r_sidecar",
        "e1r_sidecar_sleeve",
        "e1r_v0_2_backtest_summary",
        "market_entry_gate",
        "market_gate_enabled",
        "market_shock_daily_return",
        "market_shock_gate_enabled",
        "risk_off_below_spx_ma50",
        "run_stateful_simulation",
        "sidecar_active_by_regime"
      ],
      "sample_hits": [
        {
          "path": "scripts/e1r_k2_r9b_115_return_artifact_recovery.py",
          "line": 14,
          "matched": [
            "e1r_v0_2_backtest_summary"
          ],
          "text": "TARGET_ARTIFACT = ROOT / \"exports/e1r_v0_2_backtest_summary.json\""
        },
        {
          "path": "scripts/e1r_k2_r9b_115_return_artifact_recovery.py",
          "line": 26,
          "matched": [
            "e1r_sidecar",
            "e1r_sidecar_sleeve"
          ],
          "text": "    ROOT / \"src/engine/e1r_sidecar_sleeve.py\","
        },
        {
          "path": "scripts/e1r_k2_r9b_115_return_artifact_recovery.py",
          "line": 27,
          "matched": [
            "e1r_composer"
          ],
          "text": "    ROOT / \"src/engine/e1r_composer.py\","
        },
        {
          "path": "scripts/e1r_k2_r9b_115_return_artifact_recovery.py",
          "line": 45,
          "matched": [
            "116.7435999134756",
            "116.74"
          ],
          "text": "TARGET_RETURN = 116.7435999134756"
        },
        {
          "path": "scripts/e1r_k2_r9b_115_return_artifact_recovery.py",
          "line": 48,
          "matched": [
            "e1r_v0_2_backtest_summary"
          ],
          "text": "    \"e1r_v0_2_backtest_summary\","
        },
        {
          "path": "scripts/e1r_k2_r9b_115_return_artifact_recovery.py",
          "line": 49,
          "matched": [
            "E1R_REGIME_AWARE_V0_2"
          ],
          "text": "    \"E1R_REGIME_AWARE_V0_2\","
        },
        {
          "path": "scripts/e1r_k2_r9b_115_return_artifact_recovery.py",
          "line": 50,
          "matched": [
            "E1R_REGIME_AWARE_V0_1"
          ],
          "text": "    \"E1R_REGIME_AWARE_V0_1\","
        },
        {
          "path": "scripts/e1r_k2_r9b_115_return_artifact_recovery.py",
          "line": 51,
          "matched": [
            "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE"
          ],
          "text": "    \"UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE\","
        },
        {
          "path": "scripts/e1r_k2_r9b_115_return_artifact_recovery.py",
          "line": 52,
          "matched": [
            "sidecar_active_by_regime"
          ],
          "text": "    \"sidecar_active_by_regime\","
        },
        {
          "path": "scripts/e1r_k2_r9b_115_return_artifact_recovery.py",
          "line": 53,
          "matched": [
            "D3_RISK_OFF_PLUS_SHOCK_GATE"
          ],
          "text": "    \"D3_RISK_OFF_PLUS_SHOCK_GATE\","
        }
      ]
    }
  ],
  "target_artifact_has_market_gate_parameters": false,
  "target_artifact_has_regime_aware_logic": true,
  "target_artifact_has_sidecar_evidence": true
}
```

## Top Grep Paths
```json
[
  {
    "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0D_GENERATOR_PATH_TRACE.json",
    "score": 235190,
    "hit_count": 3371,
    "matched_terms": [
      "116.74",
      "116.7435999134756",
      "D3_RISK_OFF_PLUS_SHOCK_GATE",
      "E1R_REGIME_AWARE_V0_1",
      "E1R_REGIME_AWARE_V0_2",
      "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE",
      "e1r_composer",
      "e1r_sidecar",
      "e1r_sidecar_sleeve",
      "e1r_v0_2_backtest_summary",
      "market_entry_gate",
      "market_gate_enabled",
      "market_shock_daily_return",
      "market_shock_gate_enabled",
      "risk_off_below_spx_ma50",
      "run_stateful_simulation",
      "sidecar_active_by_regime"
    ],
    "sample_hits": [
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0D_GENERATOR_PATH_TRACE.json",
        "line": 30,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "        \"116.7435999134756\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0D_GENERATOR_PATH_TRACE.json",
        "line": 34,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "        \"E1R_REGIME_AWARE_V0_2\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0D_GENERATOR_PATH_TRACE.json",
        "line": 35,
        "matched": [
          "e1r_sidecar",
          "e1r_sidecar_sleeve"
        ],
        "text": "        \"build_e1r_sidecar_sleeve\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0D_GENERATOR_PATH_TRACE.json",
        "line": 43,
        "matched": [
          "e1r_v0_2_backtest_summary"
        ],
        "text": "        \"e1r_v0_2_backtest_summary.json\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0D_GENERATOR_PATH_TRACE.json",
        "line": 47,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "        \"run_stateful_simulation\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0D_GENERATOR_PATH_TRACE.json",
        "line": 339,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "            \"E1R_REGIME_AWARE_V0_2\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0D_GENERATOR_PATH_TRACE.json",
        "line": 352,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "              \"text\": \"            \\\"E1R_REGIME_AWARE_V0_2\\\"\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0D_GENERATOR_PATH_TRACE.json",
        "line": 360,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "              \"text\": \"          \\\"text\\\": \\\"- E1R_REGIME_AWARE_V0_2 formal combined daily equity records\\\"\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0D_GENERATOR_PATH_TRACE.json",
        "line": 367,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "            \"E1R_REGIME_AWARE_V0_2\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0D_GENERATOR_PATH_TRACE.json",
        "line": 372,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "              \"text\": \"            \\\"E1R_REGIME_AWARE_V0_2\\\"\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0D_GENERATOR_PATH_TRACE.json",
        "line": 380,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "              \"text\": \"          \\\"text\\\": \\\"- E1R_REGIME_AWARE_V0_2 formal combined daily equity records\\\"\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0D_GENERATOR_PATH_TRACE.json",
        "line": 816,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "            \"E1R_REGIME_AWARE_V0_2\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0D_GENERATOR_PATH_TRACE.json",
        "line": 829,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "              \"text\": \"            \\\"E1R_REGIME_AWARE_V0_2\\\"\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0D_GENERATOR_PATH_TRACE.json",
        "line": 837,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "              \"text\": \"          \\\"text\\\": \\\"        \\\\\\\"strategy_id\\\\\\\": \\\\\\\"E1R_REGIME_AWARE_V0_2\\\\\\\",\\\"\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0D_GENERATOR_PATH_TRACE.json",
        "line": 844,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "            \"E1R_REGIME_AWARE_V0_2\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0D_GENERATOR_PATH_TRACE.json",
        "line": 849,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "              \"text\": \"            \\\"E1R_REGIME_AWARE_V0_2\\\"\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0D_GENERATOR_PATH_TRACE.json",
        "line": 857,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "              \"text\": \"          \\\"text\\\": \\\"        \\\\\\\"strategy_id\\\\\\\": \\\\\\\"E1R_REGIME_AWARE_V0_2\\\\\\\",\\\"\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0D_GENERATOR_PATH_TRACE.json",
        "line": 906,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "        \"116.7435999134756\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0D_GENERATOR_PATH_TRACE.json",
        "line": 910,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "        \"E1R_REGIME_AWARE_V0_2\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0D_GENERATOR_PATH_TRACE.json",
        "line": 911,
        "matched": [
          "e1r_sidecar",
          "e1r_sidecar_sleeve"
        ],
        "text": "        \"build_e1r_sidecar_sleeve\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0D_GENERATOR_PATH_TRACE.json",
        "line": 919,
        "matched": [
          "e1r_v0_2_backtest_summary"
        ],
        "text": "        \"e1r_v0_2_backtest_summary.json\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0D_GENERATOR_PATH_TRACE.json",
        "line": 923,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "        \"run_stateful_simulation\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0D_GENERATOR_PATH_TRACE.json",
        "line": 989,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "            \"E1R_REGIME_AWARE_V0_2\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0D_GENERATOR_PATH_TRACE.json",
        "line": 1002,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "              \"text\": \"            \\\"E1R_REGIME_AWARE_V0_2\\\"\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0D_GENERATOR_PATH_TRACE.json",
        "line": 1010,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "              \"text\": \"          \\\"text\\\": \\\"- E1R_REGIME_AWARE_V0_2 formal combined daily equity records\\\"\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0D_GENERATOR_PATH_TRACE.json",
        "line": 1017,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "            \"E1R_REGIME_AWARE_V0_2\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0D_GENERATOR_PATH_TRACE.json",
        "line": 1022,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "              \"text\": \"            \\\"E1R_REGIME_AWARE_V0_2\\\"\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0D_GENERATOR_PATH_TRACE.json",
        "line": 1030,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "              \"text\": \"          \\\"text\\\": \\\"- E1R_REGIME_AWARE_V0_2 formal combined daily equity records\\\"\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0D_GENERATOR_PATH_TRACE.json",
        "line": 1438,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "            \"E1R_REGIME_AWARE_V0_2\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0D_GENERATOR_PATH_TRACE.json",
        "line": 1451,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "              \"text\": \"            \\\"E1R_REGIME_AWARE_V0_2\\\"\""
      }
    ]
  },
  {
    "path": "exports/e1_e1r_research_curve_bundle_noncanonical.json",
    "score": 100870,
    "hit_count": 1261,
    "matched_terms": [
      "116.74",
      "116.7435999134756",
      "E1R_REGIME_AWARE_V0_2"
    ],
    "sample_hits": [
      {
        "path": "exports/e1_e1r_research_curve_bundle_noncanonical.json",
        "line": 19,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "    \"strategy_id\": \"E1R_REGIME_AWARE_V0_2\","
      },
      {
        "path": "exports/e1_e1r_research_curve_bundle_noncanonical.json",
        "line": 20,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "    \"total_return_pct\": 116.7435999134756,"
      },
      {
        "path": "exports/e1_e1r_research_curve_bundle_noncanonical.json",
        "line": 10105,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2_DIRECT_COMPOSED_CANDIDATE\","
      },
      {
        "path": "exports/e1_e1r_research_curve_bundle_noncanonical.json",
        "line": 10114,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2_DIRECT_COMPOSED_CANDIDATE\","
      },
      {
        "path": "exports/e1_e1r_research_curve_bundle_noncanonical.json",
        "line": 10123,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2_DIRECT_COMPOSED_CANDIDATE\","
      },
      {
        "path": "exports/e1_e1r_research_curve_bundle_noncanonical.json",
        "line": 10132,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2_DIRECT_COMPOSED_CANDIDATE\","
      },
      {
        "path": "exports/e1_e1r_research_curve_bundle_noncanonical.json",
        "line": 10141,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2_DIRECT_COMPOSED_CANDIDATE\","
      },
      {
        "path": "exports/e1_e1r_research_curve_bundle_noncanonical.json",
        "line": 10150,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2_DIRECT_COMPOSED_CANDIDATE\","
      },
      {
        "path": "exports/e1_e1r_research_curve_bundle_noncanonical.json",
        "line": 10159,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2_DIRECT_COMPOSED_CANDIDATE\","
      },
      {
        "path": "exports/e1_e1r_research_curve_bundle_noncanonical.json",
        "line": 10168,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2_DIRECT_COMPOSED_CANDIDATE\","
      },
      {
        "path": "exports/e1_e1r_research_curve_bundle_noncanonical.json",
        "line": 10177,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2_DIRECT_COMPOSED_CANDIDATE\","
      },
      {
        "path": "exports/e1_e1r_research_curve_bundle_noncanonical.json",
        "line": 10186,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2_DIRECT_COMPOSED_CANDIDATE\","
      },
      {
        "path": "exports/e1_e1r_research_curve_bundle_noncanonical.json",
        "line": 10195,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2_DIRECT_COMPOSED_CANDIDATE\","
      },
      {
        "path": "exports/e1_e1r_research_curve_bundle_noncanonical.json",
        "line": 10204,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2_DIRECT_COMPOSED_CANDIDATE\","
      },
      {
        "path": "exports/e1_e1r_research_curve_bundle_noncanonical.json",
        "line": 10213,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2_DIRECT_COMPOSED_CANDIDATE\","
      },
      {
        "path": "exports/e1_e1r_research_curve_bundle_noncanonical.json",
        "line": 10222,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2_DIRECT_COMPOSED_CANDIDATE\","
      },
      {
        "path": "exports/e1_e1r_research_curve_bundle_noncanonical.json",
        "line": 10231,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2_DIRECT_COMPOSED_CANDIDATE\","
      },
      {
        "path": "exports/e1_e1r_research_curve_bundle_noncanonical.json",
        "line": 10240,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2_DIRECT_COMPOSED_CANDIDATE\","
      },
      {
        "path": "exports/e1_e1r_research_curve_bundle_noncanonical.json",
        "line": 10249,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2_DIRECT_COMPOSED_CANDIDATE\","
      },
      {
        "path": "exports/e1_e1r_research_curve_bundle_noncanonical.json",
        "line": 10258,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2_DIRECT_COMPOSED_CANDIDATE\","
      },
      {
        "path": "exports/e1_e1r_research_curve_bundle_noncanonical.json",
        "line": 10267,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2_DIRECT_COMPOSED_CANDIDATE\","
      },
      {
        "path": "exports/e1_e1r_research_curve_bundle_noncanonical.json",
        "line": 10276,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2_DIRECT_COMPOSED_CANDIDATE\","
      },
      {
        "path": "exports/e1_e1r_research_curve_bundle_noncanonical.json",
        "line": 10285,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2_DIRECT_COMPOSED_CANDIDATE\","
      },
      {
        "path": "exports/e1_e1r_research_curve_bundle_noncanonical.json",
        "line": 10294,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2_DIRECT_COMPOSED_CANDIDATE\","
      },
      {
        "path": "exports/e1_e1r_research_curve_bundle_noncanonical.json",
        "line": 10303,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2_DIRECT_COMPOSED_CANDIDATE\","
      },
      {
        "path": "exports/e1_e1r_research_curve_bundle_noncanonical.json",
        "line": 10312,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2_DIRECT_COMPOSED_CANDIDATE\","
      },
      {
        "path": "exports/e1_e1r_research_curve_bundle_noncanonical.json",
        "line": 10321,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2_DIRECT_COMPOSED_CANDIDATE\","
      },
      {
        "path": "exports/e1_e1r_research_curve_bundle_noncanonical.json",
        "line": 10330,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2_DIRECT_COMPOSED_CANDIDATE\","
      },
      {
        "path": "exports/e1_e1r_research_curve_bundle_noncanonical.json",
        "line": 10339,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2_DIRECT_COMPOSED_CANDIDATE\","
      },
      {
        "path": "exports/e1_e1r_research_curve_bundle_noncanonical.json",
        "line": 10348,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2_DIRECT_COMPOSED_CANDIDATE\","
      }
    ]
  },
  {
    "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
    "score": 51720,
    "hit_count": 744,
    "matched_terms": [
      "116.74",
      "116.7435999134756",
      "D3_RISK_OFF_PLUS_SHOCK_GATE",
      "E1R_REGIME_AWARE_V0_1",
      "E1R_REGIME_AWARE_V0_2",
      "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE",
      "e1r_composer",
      "e1r_sidecar",
      "e1r_sidecar_sleeve",
      "e1r_v0_2_backtest_summary",
      "market_entry_gate",
      "market_gate_enabled",
      "market_shock_daily_return",
      "market_shock_gate_enabled",
      "risk_off_below_spx_ma50",
      "sidecar_active_by_regime"
    ],
    "sample_hits": [
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 6,
        "matched": [
          "116.74"
        ],
        "text": "Find and audit the exact E1R ~116.74% full-run artifact and its market-state/gate assumptions before standalone replication."
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 11,
        "matched": [
          "e1r_v0_2_backtest_summary"
        ],
        "text": "  \"path\": \"exports/e1r_v0_2_backtest_summary.json\","
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 14,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "    \"total_return_pct\": 116.7435999134756,"
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 24,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "      \"value\": 116.7435999134756,"
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 32,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "      \"value\": 116.7435999134756"
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 64,
        "matched": [
          "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE"
        ],
        "text": "      \"value\": \"UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE\""
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 67,
        "matched": [
          "sidecar_active_by_regime"
        ],
        "text": "      \"path\": \"sidecar_active_by_regime\","
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 68,
        "matched": [
          "sidecar_active_by_regime"
        ],
        "text": "      \"key\": \"sidecar_active_by_regime\","
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 74,
        "matched": [
          "sidecar_active_by_regime"
        ],
        "text": "      \"path\": \"sidecar_active_by_regime.SIDEWAYS\","
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 83,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "      \"value\": \"E1R_REGIME_AWARE_V0_2\""
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 88,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "      \"value\": \"E1R_REGIME_AWARE_V0_2\""
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 93,
        "matched": [
          "e1r_v0_2_backtest_summary"
        ],
        "text": "      \"value\": \"exports/e1r_v0_2_backtest_summary.json\""
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 109,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "  \"total_return_pct\": 116.7435999134756,"
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 121,
        "matched": [
          "D3_RISK_OFF_PLUS_SHOCK_GATE"
        ],
        "text": "    \"market_gate_variant\": \"D3_RISK_OFF_PLUS_SHOCK_GATE\","
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 122,
        "matched": [
          "market_gate_enabled"
        ],
        "text": "    \"market_gate_enabled\": true,"
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 123,
        "matched": [
          "risk_off_below_spx_ma50"
        ],
        "text": "    \"risk_off_below_spx_ma50\": true,"
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 124,
        "matched": [
          "market_shock_gate_enabled"
        ],
        "text": "    \"market_shock_gate_enabled\": true,"
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 125,
        "matched": [
          "market_shock_daily_return"
        ],
        "text": "    \"market_shock_daily_return\": -0.02,"
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 129,
        "matched": [
          "D3_RISK_OFF_PLUS_SHOCK_GATE"
        ],
        "text": "        \"text\": \"Market Gate Variant: D3_RISK_OFF_PLUS_SHOCK_GATE\""
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 170,
        "matched": [
          "market_entry_gate"
        ],
        "text": "    \"market_entry_gate\": {"
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 171,
        "matched": [
          "D3_RISK_OFF_PLUS_SHOCK_GATE"
        ],
        "text": "      \"variant\": \"D3_RISK_OFF_PLUS_SHOCK_GATE\","
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 199,
        "matched": [
          "market_entry_gate"
        ],
        "text": "    \"market_entry_gate\": [],"
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 201,
        "matched": [
          "market_gate_enabled"
        ],
        "text": "    \"market_gate_enabled\": [],"
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 202,
        "matched": [
          "risk_off_below_spx_ma50"
        ],
        "text": "    \"risk_off_below_spx_ma50\": [],"
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 203,
        "matched": [
          "market_shock_gate_enabled"
        ],
        "text": "    \"market_shock_gate_enabled\": [],"
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 204,
        "matched": [
          "market_shock_daily_return"
        ],
        "text": "    \"market_shock_daily_return\": [],"
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 210,
        "matched": [
          "market_entry_gate"
        ],
        "text": "      \"id\": \"full_115_artifact_missing_market_entry_gate\","
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 211,
        "matched": [
          "market_entry_gate"
        ],
        "text": "      \"field\": \"market_entry_gate\","
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 220,
        "matched": [
          "market_gate_enabled"
        ],
        "text": "      \"id\": \"full_115_artifact_missing_market_gate_enabled\","
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 221,
        "matched": [
          "market_gate_enabled"
        ],
        "text": "      \"field\": \"market_gate_enabled\","
      }
    ]
  },
  {
    "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.json",
    "score": 51720,
    "hit_count": 744,
    "matched_terms": [
      "116.74",
      "116.7435999134756",
      "D3_RISK_OFF_PLUS_SHOCK_GATE",
      "E1R_REGIME_AWARE_V0_1",
      "E1R_REGIME_AWARE_V0_2",
      "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE",
      "e1r_composer",
      "e1r_sidecar",
      "e1r_sidecar_sleeve",
      "e1r_v0_2_backtest_summary",
      "market_entry_gate",
      "market_gate_enabled",
      "market_shock_daily_return",
      "market_shock_gate_enabled",
      "risk_off_below_spx_ma50",
      "sidecar_active_by_regime"
    ],
    "sample_hits": [
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.json",
        "line": 6,
        "matched": [
          "116.74"
        ],
        "text": "  \"purpose\": \"Find and audit the exact E1R ~116.74% full-run artifact and its market-state/gate assumptions before standalone replication.\","
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.json",
        "line": 32,
        "matched": [
          "e1r_v0_2_backtest_summary"
        ],
        "text": "      \"path\": \"exports/e1r_v0_2_backtest_summary.json\","
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.json",
        "line": 35,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "        \"total_return_pct\": 116.7435999134756,"
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.json",
        "line": 45,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "          \"value\": 116.7435999134756,"
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.json",
        "line": 53,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "          \"value\": 116.7435999134756"
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.json",
        "line": 85,
        "matched": [
          "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE"
        ],
        "text": "          \"value\": \"UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.json",
        "line": 88,
        "matched": [
          "sidecar_active_by_regime"
        ],
        "text": "          \"path\": \"sidecar_active_by_regime\","
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.json",
        "line": 89,
        "matched": [
          "sidecar_active_by_regime"
        ],
        "text": "          \"key\": \"sidecar_active_by_regime\","
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.json",
        "line": 95,
        "matched": [
          "sidecar_active_by_regime"
        ],
        "text": "          \"path\": \"sidecar_active_by_regime.SIDEWAYS\","
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.json",
        "line": 104,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "          \"value\": \"E1R_REGIME_AWARE_V0_2\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.json",
        "line": 109,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "          \"value\": \"E1R_REGIME_AWARE_V0_2\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.json",
        "line": 114,
        "matched": [
          "e1r_v0_2_backtest_summary"
        ],
        "text": "          \"value\": \"exports/e1r_v0_2_backtest_summary.json\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.json",
        "line": 156,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "          \"text\": \"        \\\"value\\\": 116.7435999134756,\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.json",
        "line": 160,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "          \"text\": \"        \\\"target\\\": 116.7435999134756\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.json",
        "line": 164,
        "matched": [
          "e1r_v0_2_backtest_summary"
        ],
        "text": "          \"text\": \"      \\\"path\\\": \\\"$.inspection.exports/e1r_v0_2_backtest_summary.json.metrics\\\",\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.json",
        "line": 172,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "          \"text\": \"        \\\"strategy_id\\\": \\\"E1R_REGIME_AWARE_V0_2\\\",\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.json",
        "line": 176,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "          \"text\": \"        \\\"total_return_pct\\\": 116.7435999134756,\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.json",
        "line": 196,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "          \"text\": \"        \\\"value\\\": 116.7435999134756,\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.json",
        "line": 200,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "          \"text\": \"        \\\"target\\\": 116.7435999134756\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.json",
        "line": 208,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "          \"text\": \"        \\\"strategy_id\\\": \\\"E1R_REGIME_AWARE_V0_2\\\",\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.json",
        "line": 212,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "          \"text\": \"        \\\"total_return_pct\\\": 116.7435999134756,\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.json",
        "line": 216,
        "matched": [
          "e1r_v0_2_backtest_summary"
        ],
        "text": "          \"text\": \"    \\\"file\\\": \\\"exports/e1r_v0_2_backtest_summary.json\\\"\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.json",
        "line": 232,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "          \"text\": \"        \\\"value\\\": 116.7435999134756,\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.json",
        "line": 236,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "          \"text\": \"        \\\"target\\\": 116.7435999134756\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.json",
        "line": 248,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "          \"text\": \"        \\\"total_return_pct\\\": 116.7435999134756,\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.json",
        "line": 268,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "          \"text\": \"        \\\"value\\\": 116.7435999134756,\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.json",
        "line": 272,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "          \"text\": \"        \\\"target\\\": 116.7435999134756\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.json",
        "line": 280,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "          \"text\": \"        \\\"total_return_pct\\\": 116.7435999134756,\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.json",
        "line": 300,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "          \"text\": \"        \\\"value\\\": 116.7435999134756,\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.json",
        "line": 304,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "          \"text\": \"        \\\"target\\\": 116.7435999134756\""
      }
    ]
  },
  {
    "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
    "score": 51720,
    "hit_count": 744,
    "matched_terms": [
      "116.74",
      "116.7435999134756",
      "D3_RISK_OFF_PLUS_SHOCK_GATE",
      "E1R_REGIME_AWARE_V0_1",
      "E1R_REGIME_AWARE_V0_2",
      "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE",
      "e1r_composer",
      "e1r_sidecar",
      "e1r_sidecar_sleeve",
      "e1r_v0_2_backtest_summary",
      "market_entry_gate",
      "market_gate_enabled",
      "market_shock_daily_return",
      "market_shock_gate_enabled",
      "risk_off_below_spx_ma50",
      "sidecar_active_by_regime"
    ],
    "sample_hits": [
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 6,
        "matched": [
          "116.74"
        ],
        "text": "Find and audit the exact E1R ~116.74% full-run artifact and its market-state/gate assumptions before standalone replication."
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 11,
        "matched": [
          "e1r_v0_2_backtest_summary"
        ],
        "text": "  \"path\": \"exports/e1r_v0_2_backtest_summary.json\","
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 14,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "    \"total_return_pct\": 116.7435999134756,"
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 24,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "      \"value\": 116.7435999134756,"
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 32,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "      \"value\": 116.7435999134756"
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 64,
        "matched": [
          "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE"
        ],
        "text": "      \"value\": \"UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 67,
        "matched": [
          "sidecar_active_by_regime"
        ],
        "text": "      \"path\": \"sidecar_active_by_regime\","
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 68,
        "matched": [
          "sidecar_active_by_regime"
        ],
        "text": "      \"key\": \"sidecar_active_by_regime\","
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 74,
        "matched": [
          "sidecar_active_by_regime"
        ],
        "text": "      \"path\": \"sidecar_active_by_regime.SIDEWAYS\","
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 83,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "      \"value\": \"E1R_REGIME_AWARE_V0_2\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 88,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "      \"value\": \"E1R_REGIME_AWARE_V0_2\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 93,
        "matched": [
          "e1r_v0_2_backtest_summary"
        ],
        "text": "      \"value\": \"exports/e1r_v0_2_backtest_summary.json\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 109,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "  \"total_return_pct\": 116.7435999134756,"
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 121,
        "matched": [
          "D3_RISK_OFF_PLUS_SHOCK_GATE"
        ],
        "text": "    \"market_gate_variant\": \"D3_RISK_OFF_PLUS_SHOCK_GATE\","
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 122,
        "matched": [
          "market_gate_enabled"
        ],
        "text": "    \"market_gate_enabled\": true,"
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 123,
        "matched": [
          "risk_off_below_spx_ma50"
        ],
        "text": "    \"risk_off_below_spx_ma50\": true,"
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 124,
        "matched": [
          "market_shock_gate_enabled"
        ],
        "text": "    \"market_shock_gate_enabled\": true,"
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 125,
        "matched": [
          "market_shock_daily_return"
        ],
        "text": "    \"market_shock_daily_return\": -0.02,"
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 129,
        "matched": [
          "D3_RISK_OFF_PLUS_SHOCK_GATE"
        ],
        "text": "        \"text\": \"Market Gate Variant: D3_RISK_OFF_PLUS_SHOCK_GATE\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 170,
        "matched": [
          "market_entry_gate"
        ],
        "text": "    \"market_entry_gate\": {"
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 171,
        "matched": [
          "D3_RISK_OFF_PLUS_SHOCK_GATE"
        ],
        "text": "      \"variant\": \"D3_RISK_OFF_PLUS_SHOCK_GATE\","
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 199,
        "matched": [
          "market_entry_gate"
        ],
        "text": "    \"market_entry_gate\": [],"
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 201,
        "matched": [
          "market_gate_enabled"
        ],
        "text": "    \"market_gate_enabled\": [],"
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 202,
        "matched": [
          "risk_off_below_spx_ma50"
        ],
        "text": "    \"risk_off_below_spx_ma50\": [],"
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 203,
        "matched": [
          "market_shock_gate_enabled"
        ],
        "text": "    \"market_shock_gate_enabled\": [],"
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 204,
        "matched": [
          "market_shock_daily_return"
        ],
        "text": "    \"market_shock_daily_return\": [],"
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 210,
        "matched": [
          "market_entry_gate"
        ],
        "text": "      \"id\": \"full_115_artifact_missing_market_entry_gate\","
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 211,
        "matched": [
          "market_entry_gate"
        ],
        "text": "      \"field\": \"market_entry_gate\","
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 220,
        "matched": [
          "market_gate_enabled"
        ],
        "text": "      \"id\": \"full_115_artifact_missing_market_gate_enabled\","
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 221,
        "matched": [
          "market_gate_enabled"
        ],
        "text": "      \"field\": \"market_gate_enabled\","
      }
    ]
  },
  {
    "path": "exports/e1r_engine/audit/e1r_k2_r9_market_state_115_return_artifact_audit.json",
    "score": 51720,
    "hit_count": 744,
    "matched_terms": [
      "116.74",
      "116.7435999134756",
      "D3_RISK_OFF_PLUS_SHOCK_GATE",
      "E1R_REGIME_AWARE_V0_1",
      "E1R_REGIME_AWARE_V0_2",
      "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE",
      "e1r_composer",
      "e1r_sidecar",
      "e1r_sidecar_sleeve",
      "e1r_v0_2_backtest_summary",
      "market_entry_gate",
      "market_gate_enabled",
      "market_shock_daily_return",
      "market_shock_gate_enabled",
      "risk_off_below_spx_ma50",
      "sidecar_active_by_regime"
    ],
    "sample_hits": [
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9_market_state_115_return_artifact_audit.json",
        "line": 6,
        "matched": [
          "116.74"
        ],
        "text": "  \"purpose\": \"Find and audit the exact E1R ~116.74% full-run artifact and its market-state/gate assumptions before standalone replication.\","
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9_market_state_115_return_artifact_audit.json",
        "line": 32,
        "matched": [
          "e1r_v0_2_backtest_summary"
        ],
        "text": "      \"path\": \"exports/e1r_v0_2_backtest_summary.json\","
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9_market_state_115_return_artifact_audit.json",
        "line": 35,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "        \"total_return_pct\": 116.7435999134756,"
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9_market_state_115_return_artifact_audit.json",
        "line": 45,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "          \"value\": 116.7435999134756,"
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9_market_state_115_return_artifact_audit.json",
        "line": 53,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "          \"value\": 116.7435999134756"
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9_market_state_115_return_artifact_audit.json",
        "line": 85,
        "matched": [
          "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE"
        ],
        "text": "          \"value\": \"UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE\""
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9_market_state_115_return_artifact_audit.json",
        "line": 88,
        "matched": [
          "sidecar_active_by_regime"
        ],
        "text": "          \"path\": \"sidecar_active_by_regime\","
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9_market_state_115_return_artifact_audit.json",
        "line": 89,
        "matched": [
          "sidecar_active_by_regime"
        ],
        "text": "          \"key\": \"sidecar_active_by_regime\","
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9_market_state_115_return_artifact_audit.json",
        "line": 95,
        "matched": [
          "sidecar_active_by_regime"
        ],
        "text": "          \"path\": \"sidecar_active_by_regime.SIDEWAYS\","
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9_market_state_115_return_artifact_audit.json",
        "line": 104,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "          \"value\": \"E1R_REGIME_AWARE_V0_2\""
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9_market_state_115_return_artifact_audit.json",
        "line": 109,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "          \"value\": \"E1R_REGIME_AWARE_V0_2\""
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9_market_state_115_return_artifact_audit.json",
        "line": 114,
        "matched": [
          "e1r_v0_2_backtest_summary"
        ],
        "text": "          \"value\": \"exports/e1r_v0_2_backtest_summary.json\""
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9_market_state_115_return_artifact_audit.json",
        "line": 156,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "          \"text\": \"        \\\"value\\\": 116.7435999134756,\""
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9_market_state_115_return_artifact_audit.json",
        "line": 160,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "          \"text\": \"        \\\"target\\\": 116.7435999134756\""
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9_market_state_115_return_artifact_audit.json",
        "line": 164,
        "matched": [
          "e1r_v0_2_backtest_summary"
        ],
        "text": "          \"text\": \"      \\\"path\\\": \\\"$.inspection.exports/e1r_v0_2_backtest_summary.json.metrics\\\",\""
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9_market_state_115_return_artifact_audit.json",
        "line": 172,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "          \"text\": \"        \\\"strategy_id\\\": \\\"E1R_REGIME_AWARE_V0_2\\\",\""
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9_market_state_115_return_artifact_audit.json",
        "line": 176,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "          \"text\": \"        \\\"total_return_pct\\\": 116.7435999134756,\""
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9_market_state_115_return_artifact_audit.json",
        "line": 196,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "          \"text\": \"        \\\"value\\\": 116.7435999134756,\""
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9_market_state_115_return_artifact_audit.json",
        "line": 200,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "          \"text\": \"        \\\"target\\\": 116.7435999134756\""
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9_market_state_115_return_artifact_audit.json",
        "line": 208,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "          \"text\": \"        \\\"strategy_id\\\": \\\"E1R_REGIME_AWARE_V0_2\\\",\""
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9_market_state_115_return_artifact_audit.json",
        "line": 212,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "          \"text\": \"        \\\"total_return_pct\\\": 116.7435999134756,\""
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9_market_state_115_return_artifact_audit.json",
        "line": 216,
        "matched": [
          "e1r_v0_2_backtest_summary"
        ],
        "text": "          \"text\": \"    \\\"file\\\": \\\"exports/e1r_v0_2_backtest_summary.json\\\"\""
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9_market_state_115_return_artifact_audit.json",
        "line": 232,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "          \"text\": \"        \\\"value\\\": 116.7435999134756,\""
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9_market_state_115_return_artifact_audit.json",
        "line": 236,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "          \"text\": \"        \\\"target\\\": 116.7435999134756\""
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9_market_state_115_return_artifact_audit.json",
        "line": 248,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "          \"text\": \"        \\\"total_return_pct\\\": 116.7435999134756,\""
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9_market_state_115_return_artifact_audit.json",
        "line": 268,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "          \"text\": \"        \\\"value\\\": 116.7435999134756,\""
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9_market_state_115_return_artifact_audit.json",
        "line": 272,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "          \"text\": \"        \\\"target\\\": 116.7435999134756\""
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9_market_state_115_return_artifact_audit.json",
        "line": 280,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "          \"text\": \"        \\\"total_return_pct\\\": 116.7435999134756,\""
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9_market_state_115_return_artifact_audit.json",
        "line": 300,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "          \"text\": \"        \\\"value\\\": 116.7435999134756,\""
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9_market_state_115_return_artifact_audit.json",
        "line": 304,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "          \"text\": \"        \\\"target\\\": 116.7435999134756\""
      }
    ]
  },
  {
    "path": "exports/e1r_engine/equivalence/e1r_k2_r9_115_return_market_state_parameter_compare.json",
    "score": 51720,
    "hit_count": 744,
    "matched_terms": [
      "116.74",
      "116.7435999134756",
      "D3_RISK_OFF_PLUS_SHOCK_GATE",
      "E1R_REGIME_AWARE_V0_1",
      "E1R_REGIME_AWARE_V0_2",
      "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE",
      "e1r_composer",
      "e1r_sidecar",
      "e1r_sidecar_sleeve",
      "e1r_v0_2_backtest_summary",
      "market_entry_gate",
      "market_gate_enabled",
      "market_shock_daily_return",
      "market_shock_gate_enabled",
      "risk_off_below_spx_ma50",
      "sidecar_active_by_regime"
    ],
    "sample_hits": [
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9_115_return_market_state_parameter_compare.json",
        "line": 6,
        "matched": [
          "116.74"
        ],
        "text": "  \"purpose\": \"Find and audit the exact E1R ~116.74% full-run artifact and its market-state/gate assumptions before standalone replication.\","
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9_115_return_market_state_parameter_compare.json",
        "line": 32,
        "matched": [
          "e1r_v0_2_backtest_summary"
        ],
        "text": "      \"path\": \"exports/e1r_v0_2_backtest_summary.json\","
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9_115_return_market_state_parameter_compare.json",
        "line": 35,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "        \"total_return_pct\": 116.7435999134756,"
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9_115_return_market_state_parameter_compare.json",
        "line": 45,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "          \"value\": 116.7435999134756,"
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9_115_return_market_state_parameter_compare.json",
        "line": 53,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "          \"value\": 116.7435999134756"
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9_115_return_market_state_parameter_compare.json",
        "line": 85,
        "matched": [
          "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE"
        ],
        "text": "          \"value\": \"UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE\""
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9_115_return_market_state_parameter_compare.json",
        "line": 88,
        "matched": [
          "sidecar_active_by_regime"
        ],
        "text": "          \"path\": \"sidecar_active_by_regime\","
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9_115_return_market_state_parameter_compare.json",
        "line": 89,
        "matched": [
          "sidecar_active_by_regime"
        ],
        "text": "          \"key\": \"sidecar_active_by_regime\","
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9_115_return_market_state_parameter_compare.json",
        "line": 95,
        "matched": [
          "sidecar_active_by_regime"
        ],
        "text": "          \"path\": \"sidecar_active_by_regime.SIDEWAYS\","
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9_115_return_market_state_parameter_compare.json",
        "line": 104,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "          \"value\": \"E1R_REGIME_AWARE_V0_2\""
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9_115_return_market_state_parameter_compare.json",
        "line": 109,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "          \"value\": \"E1R_REGIME_AWARE_V0_2\""
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9_115_return_market_state_parameter_compare.json",
        "line": 114,
        "matched": [
          "e1r_v0_2_backtest_summary"
        ],
        "text": "          \"value\": \"exports/e1r_v0_2_backtest_summary.json\""
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9_115_return_market_state_parameter_compare.json",
        "line": 156,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "          \"text\": \"        \\\"value\\\": 116.7435999134756,\""
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9_115_return_market_state_parameter_compare.json",
        "line": 160,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "          \"text\": \"        \\\"target\\\": 116.7435999134756\""
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9_115_return_market_state_parameter_compare.json",
        "line": 164,
        "matched": [
          "e1r_v0_2_backtest_summary"
        ],
        "text": "          \"text\": \"      \\\"path\\\": \\\"$.inspection.exports/e1r_v0_2_backtest_summary.json.metrics\\\",\""
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9_115_return_market_state_parameter_compare.json",
        "line": 172,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "          \"text\": \"        \\\"strategy_id\\\": \\\"E1R_REGIME_AWARE_V0_2\\\",\""
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9_115_return_market_state_parameter_compare.json",
        "line": 176,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "          \"text\": \"        \\\"total_return_pct\\\": 116.7435999134756,\""
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9_115_return_market_state_parameter_compare.json",
        "line": 196,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "          \"text\": \"        \\\"value\\\": 116.7435999134756,\""
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9_115_return_market_state_parameter_compare.json",
        "line": 200,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "          \"text\": \"        \\\"target\\\": 116.7435999134756\""
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9_115_return_market_state_parameter_compare.json",
        "line": 208,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "          \"text\": \"        \\\"strategy_id\\\": \\\"E1R_REGIME_AWARE_V0_2\\\",\""
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9_115_return_market_state_parameter_compare.json",
        "line": 212,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "          \"text\": \"        \\\"total_return_pct\\\": 116.7435999134756,\""
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9_115_return_market_state_parameter_compare.json",
        "line": 216,
        "matched": [
          "e1r_v0_2_backtest_summary"
        ],
        "text": "          \"text\": \"    \\\"file\\\": \\\"exports/e1r_v0_2_backtest_summary.json\\\"\""
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9_115_return_market_state_parameter_compare.json",
        "line": 232,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "          \"text\": \"        \\\"value\\\": 116.7435999134756,\""
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9_115_return_market_state_parameter_compare.json",
        "line": 236,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "          \"text\": \"        \\\"target\\\": 116.7435999134756\""
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9_115_return_market_state_parameter_compare.json",
        "line": 248,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "          \"text\": \"        \\\"total_return_pct\\\": 116.7435999134756,\""
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9_115_return_market_state_parameter_compare.json",
        "line": 268,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "          \"text\": \"        \\\"value\\\": 116.7435999134756,\""
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9_115_return_market_state_parameter_compare.json",
        "line": 272,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "          \"text\": \"        \\\"target\\\": 116.7435999134756\""
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9_115_return_market_state_parameter_compare.json",
        "line": 280,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "          \"text\": \"        \\\"total_return_pct\\\": 116.7435999134756,\""
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9_115_return_market_state_parameter_compare.json",
        "line": 300,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "          \"text\": \"        \\\"value\\\": 116.7435999134756,\""
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9_115_return_market_state_parameter_compare.json",
        "line": 304,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "          \"text\": \"        \\\"target\\\": 116.7435999134756\""
      }
    ]
  },
  {
    "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C4B_ORIGINAL_ENTRYPOINT_LOCK_REPORT.json",
    "score": 21990,
    "hit_count": 633,
    "matched_terms": [
      "116.74",
      "116.7435999134756",
      "E1R_REGIME_AWARE_V0_1",
      "E1R_REGIME_AWARE_V0_2",
      "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE",
      "e1r_composer",
      "e1r_sidecar",
      "e1r_sidecar_sleeve",
      "e1r_v0_2_backtest_summary",
      "market_entry_gate",
      "market_gate_enabled",
      "market_shock_daily_return",
      "market_shock_gate_enabled",
      "risk_off_below_spx_ma50",
      "run_stateful_simulation",
      "sidecar_active_by_regime"
    ],
    "sample_hits": [
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C4B_ORIGINAL_ENTRYPOINT_LOCK_REPORT.json",
        "line": 13,
        "matched": [
          "e1r_composer"
        ],
        "text": "      \"module\": \"src.engine.e1r_composer\","
      },
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C4B_ORIGINAL_ENTRYPOINT_LOCK_REPORT.json",
        "line": 34,
        "matched": [
          "e1r_sidecar",
          "e1r_sidecar_sleeve"
        ],
        "text": "      \"module\": \"src.engine.e1r_sidecar_sleeve\","
      },
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C4B_ORIGINAL_ENTRYPOINT_LOCK_REPORT.json",
        "line": 38,
        "matched": [
          "e1r_sidecar",
          "e1r_sidecar_sleeve"
        ],
        "text": "          \"name\": \"build_e1r_sidecar_sleeve\","
      },
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C4B_ORIGINAL_ENTRYPOINT_LOCK_REPORT.json",
        "line": 49,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "          \"name\": \"run_stateful_simulation\","
      },
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C4B_ORIGINAL_ENTRYPOINT_LOCK_REPORT.json",
        "line": 58,
        "matched": [
          "e1r_composer"
        ],
        "text": "      \"path\": \"src/engine/e1r_composer.py\","
      },
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C4B_ORIGINAL_ENTRYPOINT_LOCK_REPORT.json",
        "line": 71,
        "matched": [
          "e1r_composer"
        ],
        "text": "      \"path\": \"src/engine/e1r_composer.py\","
      },
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C4B_ORIGINAL_ENTRYPOINT_LOCK_REPORT.json",
        "line": 84,
        "matched": [
          "e1r_composer"
        ],
        "text": "      \"path\": \"src/engine/e1r_composer.py\","
      },
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C4B_ORIGINAL_ENTRYPOINT_LOCK_REPORT.json",
        "line": 98,
        "matched": [
          "E1R_REGIME_AWARE_V0_2",
          "E1R_REGIME_AWARE_V0_1",
          "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE",
          "sidecar_active_by_regime"
        ],
        "text": "      \"source_head\": \"def compose_e1r_v0_2_variant(\\n    core_variant_result: dict[str, Any],\\n    sidecar_result: dict[str, Any],\\n    initial_equity: float = 100000.0,\\n) -> dict[str, Any]:\\n    core_records = core_variant_result.get(\\\"daily_equity_records\\\", [])\\n    sidecar_records = sidecar_result.get(\\\"records\\\", [])\\n\\n    interval_records = extract_core_interval_returns(core_records, sidecar_records)\\n    equity_records = build_equity_records_from_returns(interval_records, initial_equity)\\n    summary = summarize_combined_variant(interval_records, equity_records, initial_equity)\\n\\n    result = copy.deepcopy(core_variant_result)\\n\\n    sidecar_summary = sidecar_result.get(\\\"summary\\\", {}) or {}\\n\\n    result.update({\\n        \\\"strategy_id\\\": \\\"E1R_REGIME_AWARE_V0_2\\\",\\n        \\\"strategy_variant\\\": \\\"E1R_regime_aware_v0_2_formal_sidecar_sleeve\\\",\\n        \\\"version\\\": \\\"E1R-v0.2-formal-sidecar-sleeve\\\",\\n        \\\"research_status\\\": \\\"FORMAL_SIDECAR_SLEEVE_ENGINE\\\",\\n        \\\"core_total_trades\\\": core_variant_result.get(\\\"total_trades\\\"),\\n        \\\"sidecar_trade_count_approx\\\": sidecar_summary.get(\\\"trade_count_approx\\\"),\\n        \\\"combined_trade_count_note\\\": (\\n      "
      },
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C4B_ORIGINAL_ENTRYPOINT_LOCK_REPORT.json",
        "line": 101,
        "matched": [
          "e1r_sidecar",
          "e1r_sidecar_sleeve"
        ],
        "text": "      \"path\": \"src/engine/e1r_sidecar_sleeve.py\","
      },
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C4B_ORIGINAL_ENTRYPOINT_LOCK_REPORT.json",
        "line": 117,
        "matched": [
          "e1r_sidecar",
          "e1r_sidecar_sleeve"
        ],
        "text": "      \"path\": \"src/engine/e1r_sidecar_sleeve.py\","
      },
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C4B_ORIGINAL_ENTRYPOINT_LOCK_REPORT.json",
        "line": 134,
        "matched": [
          "e1r_sidecar",
          "e1r_sidecar_sleeve"
        ],
        "text": "      \"path\": \"src/engine/e1r_sidecar_sleeve.py\","
      },
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C4B_ORIGINAL_ENTRYPOINT_LOCK_REPORT.json",
        "line": 149,
        "matched": [
          "e1r_sidecar",
          "e1r_sidecar_sleeve"
        ],
        "text": "      \"path\": \"src/engine/e1r_sidecar_sleeve.py\","
      },
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C4B_ORIGINAL_ENTRYPOINT_LOCK_REPORT.json",
        "line": 150,
        "matched": [
          "e1r_sidecar",
          "e1r_sidecar_sleeve"
        ],
        "text": "      \"function\": \"build_e1r_sidecar_sleeve\","
      },
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C4B_ORIGINAL_ENTRYPOINT_LOCK_REPORT.json",
        "line": 153,
        "matched": [
          "e1r_sidecar",
          "e1r_sidecar_sleeve"
        ],
        "text": "        \"build_e1r_sidecar_sleeve\","
      },
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C4B_ORIGINAL_ENTRYPOINT_LOCK_REPORT.json",
        "line": 163,
        "matched": [
          "e1r_sidecar",
          "e1r_sidecar_sleeve"
        ],
        "text": "      \"source_head\": \"def build_e1r_sidecar_sleeve(\\n    stock_dir: Path,\\n    spx_path: Path,\\n    regime_path: Path,\\n    config: E1RSidecarConfig,\\n) -> dict[str, Any]:\\n    spx = load_asset(spx_path)\\n    regimes = load_regimes(regime_path)\\n    stocks, excluded_found = load_stock_universe(stock_dir, config)\\n\\n    intervals = build_backtest_intervals(spx, regimes, config)\\n    rankings = build_daily_rankings(stocks, spx, regimes, intervals, config)\\n    records = run_daily_rebalanced_sidecar(rankings, spx, regimes, intervals, config)\\n    summary = summarize_sidecar(records, config)\\n\\n    regime_counts: dict[str, int] = {}\\n    subclass_counts: dict[str, int] = {}\\n\\n    for record in records:\\n        regime = record[\\\"regime\\\"]\\n        subclass = record[\\\"subclass\\\"]\\n        regime_counts[regime] = regime_counts.get(regime, 0) + 1\\n        if regime == \\\"SIDEWAYS\\\":\\n            subclass_counts[subclass] = subclass_counts.get(subclass, 0) + 1\\n\\n    return {\\n        \\\"engine\\\": \\\"e1r_sidecar_sleeve\\\",\\n        \\\"version\\\": \\\"v0.2_formal_sleeve_engine\\\",\\n        \\\"config\\\": {\\n            \\\"start_date\\\": config.start_date,\\n            \\\"end_date\\\": config.end_date,\\n   "
      },
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C4B_ORIGINAL_ENTRYPOINT_LOCK_REPORT.json",
        "line": 167,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "      \"function\": \"run_stateful_simulation\","
      },
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C4B_ORIGINAL_ENTRYPOINT_LOCK_REPORT.json",
        "line": 170,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "        \"run_stateful_simulation\","
      },
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C4B_ORIGINAL_ENTRYPOINT_LOCK_REPORT.json",
        "line": 200,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "      \"source_head\": \"def run_stateful_simulation(\\n    symbols:        list[str],\\n    prices_map:     dict[str, list[float]],\\n    dates_map:      dict[str, list[str]],\\n    spx_prices:     list[float],\\n    spx_dates:      list[str],\\n    ohlc_map:       dict = None,\\n    assumptions:    dict = None,\\n    step:           int  = 1,\\n    min_history:    int  = 120,\\n    market_score_default: float = 60.0,\\n    sim_start_date: str  = None,  # 交易执行起始日（None=从 min_history 后开始）\\n    sim_end_date:   str  = None,  # 交易执行截止日（None=到末尾）\\n    ndx_prices:     list = None,  # NDX 收盘价（Gate v2 Leadership 判断）\\n    ndx_dates:      list = None,\\n    sox_prices:     list = None,  # SOX 收盘价\\n    sox_dates:      list = None,\\n    vix_prices:     list = None,  # VIX 收盘价\\n    vix_dates:      list = None,\\n) -> dict:\\n    \\\"\\\"\\\"\\n    Layer D v1.6: Strict Top3 + RS threshold + MinHold + Relative SPX Stop\\n\\n    修正项（相比 v3）：\\n    1. SPX master calendar — 时间轴以 SPX dates 为准\\n    2. Date-based alignment — 所有股票按日期查找，不用 index 直接对齐\\n    3. skipped_orders_by_reason — 跳过原因分类统计\\n    4. sample_validity 检查 — 样本不足时返回 INSUFFICIENT_SAMPLE\\n    \\\"\\\"\\\"\\n    logger.info(\\\"[Backtest Layer D v1.6] Strict Top3 + RS/MinHold/Rel"
      },
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C4B_ORIGINAL_ENTRYPOINT_LOCK_REPORT.json",
        "line": 208,
        "matched": [
          "e1r_sidecar",
          "e1r_sidecar_sleeve"
        ],
        "text": "        \"build_e1r_sidecar_sleeve\","
      },
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C4B_ORIGINAL_ENTRYPOINT_LOCK_REPORT.json",
        "line": 209,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "        \"run_stateful_simulation\","
      },
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C4B_ORIGINAL_ENTRYPOINT_LOCK_REPORT.json",
        "line": 229,
        "matched": [
          "market_gate_enabled",
          "risk_off_below_spx_ma50",
          "market_shock_gate_enabled",
          "market_shock_daily_return"
        ],
        "text": "      \"source_head\": \"def run_strategy_variant_comparison(\\n    symbols: list[str],\\n    prices_map: dict[str, list[float]],\\n    dates_map: dict[str, list[str]],\\n    spx_prices: list[float],\\n    spx_dates: list[str],\\n    ndx_prices: list[float] = None,\\n    ndx_dates:  list[str]   = None,\\n    sox_prices: list[float] = None,\\n    sox_dates:  list[str]   = None,\\n    vix_prices: list[float] = None,\\n    vix_dates:  list[str]   = None,\\n) -> dict:\\n    \\\"\\\"\\\"\\n    Run four diagnostic portfolio variants using Strict Top3, no fixed TP.\\n\\n    V0_BASE: current Strict Top3 baseline.\\n    V1_RS95: raise entry RS threshold from 90 to 95.\\n    V2_RS95_MINHOLD5: add minimum 5 trading-day hold for ordinary REDUCE/EXIT.\\n    V3_RS95_MINHOLD5_RELSTOP8: add relative SPX underperformance stop.\\n\\n    Selection policy:\\n    1. Prefer PASS over PARTIAL over FAIL.\\n    2. Within the same status, prefer higher total return.\\n    3. Break ties with higher Profit Factor, higher Sharpe, then lower max drawdown.\\n    \\\"\\\"\\\"\\n    logger.info(\\\"[Backtest Layer D v1.6] Strategy Variant Comparison...\\\")\\n\\n    base = {\\n        **LAYER_D_ASSUMPTIONS,\\n        \\\"market_gate_enabled\\\": False,\\n        \\\"ma"
      },
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C4B_ORIGINAL_ENTRYPOINT_LOCK_REPORT.json",
        "line": 261,
        "matched": [
          "e1r_composer"
        ],
        "text": "      \"path\": \"src/engine/e1r_composer.py\","
      },
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C4B_ORIGINAL_ENTRYPOINT_LOCK_REPORT.json",
        "line": 373,
        "matched": [
          "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE"
        ],
        "text": "          \"text\": \"\\\"regime_aware_logic\\\": \\\"UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE\\\",\","
      },
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C4B_ORIGINAL_ENTRYPOINT_LOCK_REPORT.json",
        "line": 389,
        "matched": [
          "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE"
        ],
        "text": "              \"text\": \"        \\\"regime_aware_logic\\\": \\\"UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE\\\",\""
      },
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C4B_ORIGINAL_ENTRYPOINT_LOCK_REPORT.json",
        "line": 397,
        "matched": [
          "E1R_REGIME_AWARE_V0_1"
        ],
        "text": "              \"text\": \"        \\\"e1r_v0_2_core_variant\\\": \\\"E1R_REGIME_AWARE_V0_1\\\",\""
      },
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C4B_ORIGINAL_ENTRYPOINT_LOCK_REPORT.json",
        "line": 408,
        "matched": [
          "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE"
        ],
        "text": "          \"text\": \"\\\"regime_aware_logic\\\": \\\"UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE\\\",\","
      },
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C4B_ORIGINAL_ENTRYPOINT_LOCK_REPORT.json",
        "line": 424,
        "matched": [
          "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE"
        ],
        "text": "              \"text\": \"        \\\"regime_aware_logic\\\": \\\"UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE\\\",\""
      },
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C4B_ORIGINAL_ENTRYPOINT_LOCK_REPORT.json",
        "line": 432,
        "matched": [
          "E1R_REGIME_AWARE_V0_1"
        ],
        "text": "              \"text\": \"        \\\"e1r_v0_2_core_variant\\\": \\\"E1R_REGIME_AWARE_V0_1\\\",\""
      },
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C4B_ORIGINAL_ENTRYPOINT_LOCK_REPORT.json",
        "line": 447,
        "matched": [
          "E1R_REGIME_AWARE_V0_1"
        ],
        "text": "              \"text\": \"        \\\"e1r_v0_2_core_variant\\\": \\\"E1R_REGIME_AWARE_V0_1\\\",\""
      },
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C4B_ORIGINAL_ENTRYPOINT_LOCK_REPORT.json",
        "line": 478,
        "matched": [
          "e1r_sidecar",
          "e1r_sidecar_sleeve"
        ],
        "text": "      \"path\": \"src/engine/e1r_sidecar_sleeve.py\","
      }
    ]
  },
  {
    "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0J_COMPOSER_CALLSITE_INSTRUMENTATION.json",
    "score": 17490,
    "hit_count": 316,
    "matched_terms": [
      "116.74",
      "116.7435999134756",
      "E1R_REGIME_AWARE_V0_1",
      "E1R_REGIME_AWARE_V0_2",
      "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE",
      "e1r_composer",
      "e1r_sidecar",
      "e1r_sidecar_sleeve",
      "e1r_v0_2_backtest_summary",
      "run_stateful_simulation",
      "sidecar_active_by_regime"
    ],
    "sample_hits": [
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0J_COMPOSER_CALLSITE_INSTRUMENTATION.json",
        "line": 4,
        "matched": [
          "e1r_composer"
        ],
        "text": "  \"status\": \"E1R_COMPOSER_CALLSITE_INSTRUMENTATION_COMPLETE_OUTPUTS_RESTORED\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0J_COMPOSER_CALLSITE_INSTRUMENTATION.json",
        "line": 231,
        "matched": [
          "e1r_sidecar",
          "e1r_sidecar_sleeve"
        ],
        "text": "                \"text\": \"    \\\"build_e1r_sidecar_sleeve\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0J_COMPOSER_CALLSITE_INSTRUMENTATION.json",
        "line": 239,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "                \"text\": \"    \\\"run_stateful_simulation\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0J_COMPOSER_CALLSITE_INSTRUMENTATION.json",
        "line": 271,
        "matched": [
          "e1r_sidecar",
          "e1r_sidecar_sleeve"
        ],
        "text": "                \"text\": \"    \\\"build_e1r_sidecar_sleeve\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0J_COMPOSER_CALLSITE_INSTRUMENTATION.json",
        "line": 279,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "                \"text\": \"    \\\"run_stateful_simulation\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0J_COMPOSER_CALLSITE_INSTRUMENTATION.json",
        "line": 283,
        "matched": [
          "e1r_v0_2_backtest_summary"
        ],
        "text": "                \"text\": \"    \\\"e1r_v0_2_backtest_summary.json\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0J_COMPOSER_CALLSITE_INSTRUMENTATION.json",
        "line": 307,
        "matched": [
          "e1r_sidecar",
          "e1r_sidecar_sleeve"
        ],
        "text": "                \"text\": \"    \\\"build_e1r_sidecar_sleeve\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0J_COMPOSER_CALLSITE_INSTRUMENTATION.json",
        "line": 315,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "                \"text\": \"    \\\"run_stateful_simulation\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0J_COMPOSER_CALLSITE_INSTRUMENTATION.json",
        "line": 319,
        "matched": [
          "e1r_v0_2_backtest_summary"
        ],
        "text": "                \"text\": \"    \\\"e1r_v0_2_backtest_summary.json\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0J_COMPOSER_CALLSITE_INSTRUMENTATION.json",
        "line": 327,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "                \"text\": \"    \\\"E1R_REGIME_AWARE_V0_2\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0J_COMPOSER_CALLSITE_INSTRUMENTATION.json",
        "line": 334,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "              \"run_stateful_simulation\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0J_COMPOSER_CALLSITE_INSTRUMENTATION.json",
        "line": 347,
        "matched": [
          "e1r_sidecar",
          "e1r_sidecar_sleeve"
        ],
        "text": "                \"text\": \"    \\\"build_e1r_sidecar_sleeve\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0J_COMPOSER_CALLSITE_INSTRUMENTATION.json",
        "line": 355,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "                \"text\": \"    \\\"run_stateful_simulation\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0J_COMPOSER_CALLSITE_INSTRUMENTATION.json",
        "line": 359,
        "matched": [
          "e1r_v0_2_backtest_summary"
        ],
        "text": "                \"text\": \"    \\\"e1r_v0_2_backtest_summary.json\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0J_COMPOSER_CALLSITE_INSTRUMENTATION.json",
        "line": 367,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "                \"text\": \"    \\\"E1R_REGIME_AWARE_V0_2\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0J_COMPOSER_CALLSITE_INSTRUMENTATION.json",
        "line": 378,
        "matched": [
          "e1r_v0_2_backtest_summary"
        ],
        "text": "              \"e1r_v0_2_backtest_summary.json\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0J_COMPOSER_CALLSITE_INSTRUMENTATION.json",
        "line": 387,
        "matched": [
          "e1r_sidecar",
          "e1r_sidecar_sleeve"
        ],
        "text": "                \"text\": \"    \\\"build_e1r_sidecar_sleeve\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0J_COMPOSER_CALLSITE_INSTRUMENTATION.json",
        "line": 395,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "                \"text\": \"    \\\"run_stateful_simulation\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0J_COMPOSER_CALLSITE_INSTRUMENTATION.json",
        "line": 399,
        "matched": [
          "e1r_v0_2_backtest_summary"
        ],
        "text": "                \"text\": \"    \\\"e1r_v0_2_backtest_summary.json\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0J_COMPOSER_CALLSITE_INSTRUMENTATION.json",
        "line": 407,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "                \"text\": \"    \\\"E1R_REGIME_AWARE_V0_2\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0J_COMPOSER_CALLSITE_INSTRUMENTATION.json",
        "line": 427,
        "matched": [
          "e1r_sidecar",
          "e1r_sidecar_sleeve"
        ],
        "text": "                \"text\": \"    \\\"build_e1r_sidecar_sleeve\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0J_COMPOSER_CALLSITE_INSTRUMENTATION.json",
        "line": 435,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "                \"text\": \"    \\\"run_stateful_simulation\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0J_COMPOSER_CALLSITE_INSTRUMENTATION.json",
        "line": 439,
        "matched": [
          "e1r_v0_2_backtest_summary"
        ],
        "text": "                \"text\": \"    \\\"e1r_v0_2_backtest_summary.json\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0J_COMPOSER_CALLSITE_INSTRUMENTATION.json",
        "line": 447,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "                \"text\": \"    \\\"E1R_REGIME_AWARE_V0_2\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0J_COMPOSER_CALLSITE_INSTRUMENTATION.json",
        "line": 466,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "              \"E1R_REGIME_AWARE_V0_2\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0J_COMPOSER_CALLSITE_INSTRUMENTATION.json",
        "line": 475,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "                \"text\": \"    \\\"run_stateful_simulation\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0J_COMPOSER_CALLSITE_INSTRUMENTATION.json",
        "line": 479,
        "matched": [
          "e1r_v0_2_backtest_summary"
        ],
        "text": "                \"text\": \"    \\\"e1r_v0_2_backtest_summary.json\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0J_COMPOSER_CALLSITE_INSTRUMENTATION.json",
        "line": 487,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "                \"text\": \"    \\\"E1R_REGIME_AWARE_V0_2\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0J_COMPOSER_CALLSITE_INSTRUMENTATION.json",
        "line": 1214,
        "matched": [
          "e1r_v0_2_backtest_summary"
        ],
        "text": "              \"e1r_v0_2_backtest_summary.json\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0J_COMPOSER_CALLSITE_INSTRUMENTATION.json",
        "line": 1236,
        "matched": [
          "e1r_v0_2_backtest_summary"
        ],
        "text": "                \"text\": \"    if \\\"e1r_v0_2_backtest_equity_curve.json\\\" in generator_text and \\\"e1r_v0_2_backtest_summary.json\\\" in generator_text:\""
      }
    ]
  },
  {
    "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json",
    "score": 12260,
    "hit_count": 259,
    "matched_terms": [
      "116.74",
      "116.7435999134756",
      "E1R_REGIME_AWARE_V0_1",
      "E1R_REGIME_AWARE_V0_2",
      "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE",
      "e1r_composer",
      "e1r_sidecar",
      "e1r_sidecar_sleeve",
      "e1r_v0_2_backtest_summary",
      "market_entry_gate",
      "market_gate_enabled",
      "market_shock_daily_return",
      "market_shock_gate_enabled",
      "risk_off_below_spx_ma50",
      "run_stateful_simulation",
      "sidecar_active_by_regime"
    ],
    "sample_hits": [
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json",
        "line": 14,
        "matched": [
          "e1r_composer"
        ],
        "text": "    \"src/engine/e1r_composer.py\": {"
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json",
        "line": 20,
        "matched": [
          "E1R_REGIME_AWARE_V0_1"
        ],
        "text": "            \"E1R_REGIME_AWARE_V0_1\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json",
        "line": 22,
        "matched": [
          "E1R_REGIME_AWARE_V0_1"
        ],
        "text": "          \"text\": \"- E1R_REGIME_AWARE_V0_1 core daily equity records\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json",
        "line": 27,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "            \"E1R_REGIME_AWARE_V0_2\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json",
        "line": 29,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "          \"text\": \"- E1R_REGIME_AWARE_V0_2 formal combined daily equity records\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json",
        "line": 553,
        "matched": [
          "sidecar_active_by_regime"
        ],
        "text": "          \"text\": \"        \\\"sidecar_active_by_regime\\\": active_by_regime,\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json",
        "line": 594,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "            \"E1R_REGIME_AWARE_V0_2\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json",
        "line": 596,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "          \"text\": \"        \\\"strategy_id\\\": \\\"E1R_REGIME_AWARE_V0_2\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json",
        "line": 601,
        "matched": [
          "E1R_REGIME_AWARE_V0_1"
        ],
        "text": "            \"E1R_REGIME_AWARE_V0_1\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json",
        "line": 603,
        "matched": [
          "E1R_REGIME_AWARE_V0_1"
        ],
        "text": "          \"text\": \"            \\\"core_variant\\\": \\\"E1R_REGIME_AWARE_V0_1\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json",
        "line": 654,
        "matched": [
          "sidecar_active_by_regime"
        ],
        "text": "          \"text\": \"    result[\\\"sidecar_active_by_regime\\\"] = summary[\\\"sidecar_active_by_regime\\\"]\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json",
        "line": 668,
        "matched": [
          "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE"
        ],
        "text": "          \"text\": \"        \\\"regime_aware_logic\\\": \\\"UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json",
        "line": 673,
        "matched": [
          "E1R_REGIME_AWARE_V0_1"
        ],
        "text": "            \"E1R_REGIME_AWARE_V0_1\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json",
        "line": 675,
        "matched": [
          "E1R_REGIME_AWARE_V0_1"
        ],
        "text": "          \"text\": \"        \\\"e1r_v0_2_core_variant\\\": \\\"E1R_REGIME_AWARE_V0_1\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json",
        "line": 783,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "            \"E1R_REGIME_AWARE_V0_2\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json",
        "line": 784,
        "matched": [
          "E1R_REGIME_AWARE_V0_1"
        ],
        "text": "            \"E1R_REGIME_AWARE_V0_1\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json",
        "line": 786,
        "matched": [
          "E1R_REGIME_AWARE_V0_2",
          "E1R_REGIME_AWARE_V0_1"
        ],
        "text": "          \"source_head\": \"def compose_e1r_v0_2_variant(\\n    core_variant_result: dict[str, Any],\\n    sidecar_result: dict[str, Any],\\n    initial_equity: float = 100000.0,\\n) -> dict[str, Any]:\\n    core_records = core_variant_result.get(\\\"daily_equity_records\\\", [])\\n    sidecar_records = sidecar_result.get(\\\"records\\\", [])\\n\\n    interval_records = extract_core_interval_returns(core_records, sidecar_records)\\n    equity_records = build_equity_records_from_returns(interval_records, initial_equity)\\n    summary = summarize_combined_variant(interval_records, equity_records, initial_equity)\\n\\n    result = copy.deepcopy(core_variant_result)\\n\\n    sidecar_summary = sidecar_result.get(\\\"summary\\\", {}) or {}\\n\\n    result.update({\\n        \\\"strategy_id\\\": \\\"E1R_REGIME_AWARE_V0_2\\\",\\n        \\\"strategy_variant\\\": \\\"E1R_regime_aware_v0_2_formal_sidecar_sleeve\\\",\\n        \\\"version\\\": \\\"E1R-v0.2-formal-sidecar-sleeve\\\",\\n        \\\"research_status\\\": \\\"FORMAL_SIDECAR_SLEEVE_ENGINE\\\",\\n        \\\"core_total_trades\\\": core_variant_result.get(\\\"total_trades\\\"),\\n        \\\"sidecar_trade_count_approx\\\": sidecar_summary.get(\\\"trade_count_approx\\\"),\\n        \\\"combined_trade_count_note\\\": (\\n  "
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json",
        "line": 790,
        "matched": [
          "e1r_sidecar",
          "e1r_sidecar_sleeve"
        ],
        "text": "    \"src/engine/e1r_sidecar_sleeve.py\": {"
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json",
        "line": 796,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "            \"E1R_REGIME_AWARE_V0_2\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json",
        "line": 798,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "          \"text\": \"Formal engine module for E1R_REGIME_AWARE_V0_2 sidecar sleeve.\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json",
        "line": 810,
        "matched": [
          "E1R_REGIME_AWARE_V0_1"
        ],
        "text": "            \"E1R_REGIME_AWARE_V0_1\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json",
        "line": 812,
        "matched": [
          "E1R_REGIME_AWARE_V0_1"
        ],
        "text": "          \"text\": \"- E1R_REGIME_AWARE_V0_1 core\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json",
        "line": 1038,
        "matched": [
          "e1r_sidecar",
          "e1r_sidecar_sleeve"
        ],
        "text": "          \"name\": \"build_e1r_sidecar_sleeve\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json",
        "line": 1050,
        "matched": [
          "e1r_sidecar",
          "e1r_sidecar_sleeve"
        ],
        "text": "          \"source_head\": \"def build_e1r_sidecar_sleeve(\\n    stock_dir: Path,\\n    spx_path: Path,\\n    regime_path: Path,\\n    config: E1RSidecarConfig,\\n) -> dict[str, Any]:\\n    spx = load_asset(spx_path)\\n    regimes = load_regimes(regime_path)\\n    stocks, excluded_found = load_stock_universe(stock_dir, config)\\n\\n    intervals = build_backtest_intervals(spx, regimes, config)\\n    rankings = build_daily_rankings(stocks, spx, regimes, intervals, config)\\n    records = run_daily_rebalanced_sidecar(rankings, spx, regimes, intervals, config)\\n    summary = summarize_sidecar(records, config)\\n\\n    regime_counts: dict[str, int] = {}\\n    subclass_counts: dict[str, int] = {}\\n\\n    for record in records:\\n        regime = record[\\\"regime\\\"]\\n        subclass = record[\\\"subclass\\\"]\\n        regime_counts[regime] = regime_counts.get(regime, 0) + 1\\n        if regime == \\\"SIDEWAYS\\\":\\n            subclass_counts[subclass] = subclass_counts.get(subclass, 0) + 1\\n\\n    return {\\n        \\\"engine\\\": \\\"e1r_sidecar_sleeve\\\",\\n        \\\"version\\\": \\\"v0.2_formal_sleeve_engine\\\",\\n        \\\"config\\\": {\\n            \\\"start_date\\\": config.start_date,\\n            \\\"end_date\\\": config.end_date,\\"
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json",
        "line": 1266,
        "matched": [
          "E1R_REGIME_AWARE_V0_1"
        ],
        "text": "            \"E1R_REGIME_AWARE_V0_1\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json",
        "line": 1268,
        "matched": [
          "E1R_REGIME_AWARE_V0_1"
        ],
        "text": "          \"text\": \"        \\\"E1R_REGIME_AWARE_V0_1\\\": {\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json",
        "line": 1273,
        "matched": [
          "E1R_REGIME_AWARE_V0_1"
        ],
        "text": "            \"E1R_REGIME_AWARE_V0_1\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json",
        "line": 1275,
        "matched": [
          "E1R_REGIME_AWARE_V0_1"
        ],
        "text": "          \"text\": \"    # - Do not modify E1R_REGIME_AWARE_V0_1.\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json",
        "line": 1287,
        "matched": [
          "E1R_REGIME_AWARE_V0_1"
        ],
        "text": "            \"E1R_REGIME_AWARE_V0_1\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json",
        "line": 1289,
        "matched": [
          "E1R_REGIME_AWARE_V0_1"
        ],
        "text": "          \"text\": \"        _core_e1r = variant_results.get(\\\"E1R_REGIME_AWARE_V0_1\\\")\""
      }
    ]
  },
  {
    "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C2_RECOVER_5Y_PORTFOLIO_EQUITY_CANDIDATES.json",
    "score": 11420,
    "hit_count": 224,
    "matched_terms": [
      "116.74",
      "116.7435999134756",
      "E1R_REGIME_AWARE_V0_1",
      "E1R_REGIME_AWARE_V0_2",
      "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE",
      "e1r_composer",
      "e1r_sidecar",
      "e1r_sidecar_sleeve",
      "e1r_v0_2_backtest_summary",
      "market_entry_gate",
      "sidecar_active_by_regime"
    ],
    "sample_hits": [
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C2_RECOVER_5Y_PORTFOLIO_EQUITY_CANDIDATES.json",
        "line": 20,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "        \"E1R_REGIME_AWARE_V0_2\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C2_RECOVER_5Y_PORTFOLIO_EQUITY_CANDIDATES.json",
        "line": 22,
        "matched": [
          "116.74"
        ],
        "text": "        \"116.74\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C2_RECOVER_5Y_PORTFOLIO_EQUITY_CANDIDATES.json",
        "line": 550,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "        \"E1R_REGIME_AWARE_V0_2\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C2_RECOVER_5Y_PORTFOLIO_EQUITY_CANDIDATES.json",
        "line": 1028,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "          \"list_path\": \"source_reports.scripts/run_e1r_v0_2_oos.py.term_hits.E1R_REGIME_AWARE_V0_2\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C2_RECOVER_5Y_PORTFOLIO_EQUITY_CANDIDATES.json",
        "line": 1061,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "        \"E1R_REGIME_AWARE_V0_2\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C2_RECOVER_5Y_PORTFOLIO_EQUITY_CANDIDATES.json",
        "line": 1064,
        "matched": [
          "116.74"
        ],
        "text": "        \"116.74\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C2_RECOVER_5Y_PORTFOLIO_EQUITY_CANDIDATES.json",
        "line": 1362,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "          \"list_path\": \"watched_file_reports.src/engine/backtest.py.hits.E1R_REGIME_AWARE_V0_2\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C2_RECOVER_5Y_PORTFOLIO_EQUITY_CANDIDATES.json",
        "line": 2027,
        "matched": [
          "market_entry_gate"
        ],
        "text": "          \"list_path\": \"market_entry_gate.blocked_actions\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C2_RECOVER_5Y_PORTFOLIO_EQUITY_CANDIDATES.json",
        "line": 2044,
        "matched": [
          "market_entry_gate"
        ],
        "text": "          \"list_path\": \"market_entry_gate.unaffected_actions\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C2_RECOVER_5Y_PORTFOLIO_EQUITY_CANDIDATES.json",
        "line": 2172,
        "matched": [
          "market_entry_gate"
        ],
        "text": "          \"list_path\": \"variant_results.E1_AUDITED_G4_MINHOLD10.market_entry_gate.blocked_actions\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C2_RECOVER_5Y_PORTFOLIO_EQUITY_CANDIDATES.json",
        "line": 2189,
        "matched": [
          "market_entry_gate"
        ],
        "text": "          \"list_path\": \"variant_results.E1_AUDITED_G4_MINHOLD10.market_entry_gate.unaffected_actions\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C2_RECOVER_5Y_PORTFOLIO_EQUITY_CANDIDATES.json",
        "line": 2401,
        "matched": [
          "market_entry_gate"
        ],
        "text": "          \"list_path\": \"variant_results.E2_DYNAMIC_EXIT_V2.market_entry_gate.blocked_actions\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C2_RECOVER_5Y_PORTFOLIO_EQUITY_CANDIDATES.json",
        "line": 2418,
        "matched": [
          "market_entry_gate"
        ],
        "text": "          \"list_path\": \"variant_results.E2_DYNAMIC_EXIT_V2.market_entry_gate.unaffected_actions\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C2_RECOVER_5Y_PORTFOLIO_EQUITY_CANDIDATES.json",
        "line": 2665,
        "matched": [
          "market_entry_gate"
        ],
        "text": "          \"list_path\": \"backtest.results.layer_d.market_entry_gate.blocked_actions\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C2_RECOVER_5Y_PORTFOLIO_EQUITY_CANDIDATES.json",
        "line": 2682,
        "matched": [
          "market_entry_gate"
        ],
        "text": "          \"list_path\": \"backtest.results.layer_d.market_entry_gate.unaffected_actions\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C2_RECOVER_5Y_PORTFOLIO_EQUITY_CANDIDATES.json",
        "line": 2936,
        "matched": [
          "market_entry_gate"
        ],
        "text": "          \"list_path\": \"backtest.results.layer_d.variant_results.E1_AUDITED_G4_MINHOLD10.market_entry_gate.blocked_actions\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C2_RECOVER_5Y_PORTFOLIO_EQUITY_CANDIDATES.json",
        "line": 2953,
        "matched": [
          "market_entry_gate"
        ],
        "text": "          \"list_path\": \"backtest.results.layer_d.variant_results.E1_AUDITED_G4_MINHOLD10.market_entry_gate.unaffected_actions\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C2_RECOVER_5Y_PORTFOLIO_EQUITY_CANDIDATES.json",
        "line": 3165,
        "matched": [
          "market_entry_gate"
        ],
        "text": "          \"list_path\": \"backtest.results.layer_d.variant_results.E2_DYNAMIC_EXIT_V2.market_entry_gate.blocked_actions\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C2_RECOVER_5Y_PORTFOLIO_EQUITY_CANDIDATES.json",
        "line": 3182,
        "matched": [
          "market_entry_gate"
        ],
        "text": "          \"list_path\": \"backtest.results.layer_d.variant_results.E2_DYNAMIC_EXIT_V2.market_entry_gate.unaffected_actions\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C2_RECOVER_5Y_PORTFOLIO_EQUITY_CANDIDATES.json",
        "line": 3231,
        "matched": [
          "116.74"
        ],
        "text": "        \"116.74\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C2_RECOVER_5Y_PORTFOLIO_EQUITY_CANDIDATES.json",
        "line": 3299,
        "matched": [
          "116.74"
        ],
        "text": "        \"116.74\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C2_RECOVER_5Y_PORTFOLIO_EQUITY_CANDIDATES.json",
        "line": 3367,
        "matched": [
          "116.74"
        ],
        "text": "        \"116.74\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C2_RECOVER_5Y_PORTFOLIO_EQUITY_CANDIDATES.json",
        "line": 3434,
        "matched": [
          "116.74"
        ],
        "text": "        \"116.74\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C2_RECOVER_5Y_PORTFOLIO_EQUITY_CANDIDATES.json",
        "line": 3501,
        "matched": [
          "116.74"
        ],
        "text": "        \"116.74\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C2_RECOVER_5Y_PORTFOLIO_EQUITY_CANDIDATES.json",
        "line": 3568,
        "matched": [
          "116.74"
        ],
        "text": "        \"116.74\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C2_RECOVER_5Y_PORTFOLIO_EQUITY_CANDIDATES.json",
        "line": 3635,
        "matched": [
          "116.74"
        ],
        "text": "        \"116.74\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C2_RECOVER_5Y_PORTFOLIO_EQUITY_CANDIDATES.json",
        "line": 3702,
        "matched": [
          "116.74"
        ],
        "text": "        \"116.74\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C2_RECOVER_5Y_PORTFOLIO_EQUITY_CANDIDATES.json",
        "line": 3769,
        "matched": [
          "116.74"
        ],
        "text": "        \"116.74\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C2_RECOVER_5Y_PORTFOLIO_EQUITY_CANDIDATES.json",
        "line": 3836,
        "matched": [
          "116.74"
        ],
        "text": "        \"116.74\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C2_RECOVER_5Y_PORTFOLIO_EQUITY_CANDIDATES.json",
        "line": 3903,
        "matched": [
          "116.74"
        ],
        "text": "        \"116.74\","
      }
    ]
  },
  {
    "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0K_TRUE_COMPOSER_CALLSITE_TRACE.json",
    "score": 10820,
    "hit_count": 235,
    "matched_terms": [
      "E1R_REGIME_AWARE_V0_1",
      "E1R_REGIME_AWARE_V0_2",
      "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE",
      "e1r_composer",
      "e1r_sidecar",
      "e1r_sidecar_sleeve",
      "e1r_v0_2_backtest_summary",
      "run_stateful_simulation"
    ],
    "sample_hits": [
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0K_TRUE_COMPOSER_CALLSITE_TRACE.json",
        "line": 24,
        "matched": [
          "e1r_composer"
        ],
        "text": "      \"path\": \"src/engine/e1r_composer.py\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0K_TRUE_COMPOSER_CALLSITE_TRACE.json",
        "line": 31,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "            \"E1R_REGIME_AWARE_V0_2\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0K_TRUE_COMPOSER_CALLSITE_TRACE.json",
        "line": 40,
        "matched": [
          "E1R_REGIME_AWARE_V0_1"
        ],
        "text": "              \"text\": \"- E1R_REGIME_AWARE_V0_1 core daily equity records\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0K_TRUE_COMPOSER_CALLSITE_TRACE.json",
        "line": 56,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "              \"text\": \"- E1R_REGIME_AWARE_V0_2 formal combined daily equity records\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0K_TRUE_COMPOSER_CALLSITE_TRACE.json",
        "line": 596,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "              \"text\": \"        \\\"strategy_id\\\": \\\"E1R_REGIME_AWARE_V0_2\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0K_TRUE_COMPOSER_CALLSITE_TRACE.json",
        "line": 640,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "              \"text\": \"        \\\"strategy_id\\\": \\\"E1R_REGIME_AWARE_V0_2\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0K_TRUE_COMPOSER_CALLSITE_TRACE.json",
        "line": 644,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "              \"text\": \"        \\\"strategy_variant\\\": \\\"E1R_regime_aware_v0_2_formal_sidecar_sleeve\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0K_TRUE_COMPOSER_CALLSITE_TRACE.json",
        "line": 655,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "            \"E1R_REGIME_AWARE_V0_2\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0K_TRUE_COMPOSER_CALLSITE_TRACE.json",
        "line": 680,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "              \"text\": \"        \\\"strategy_id\\\": \\\"E1R_REGIME_AWARE_V0_2\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0K_TRUE_COMPOSER_CALLSITE_TRACE.json",
        "line": 684,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "              \"text\": \"        \\\"strategy_variant\\\": \\\"E1R_regime_aware_v0_2_formal_sidecar_sleeve\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0K_TRUE_COMPOSER_CALLSITE_TRACE.json",
        "line": 716,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "              \"text\": \"        \\\"strategy_id\\\": \\\"E1R_REGIME_AWARE_V0_2\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0K_TRUE_COMPOSER_CALLSITE_TRACE.json",
        "line": 720,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "              \"text\": \"        \\\"strategy_variant\\\": \\\"E1R_regime_aware_v0_2_formal_sidecar_sleeve\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0K_TRUE_COMPOSER_CALLSITE_TRACE.json",
        "line": 780,
        "matched": [
          "E1R_REGIME_AWARE_V0_1"
        ],
        "text": "              \"text\": \"            \\\"core_variant\\\": \\\"E1R_REGIME_AWARE_V0_1\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0K_TRUE_COMPOSER_CALLSITE_TRACE.json",
        "line": 828,
        "matched": [
          "E1R_REGIME_AWARE_V0_1"
        ],
        "text": "              \"text\": \"            \\\"core_variant\\\": \\\"E1R_REGIME_AWARE_V0_1\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0K_TRUE_COMPOSER_CALLSITE_TRACE.json",
        "line": 868,
        "matched": [
          "E1R_REGIME_AWARE_V0_1"
        ],
        "text": "              \"text\": \"            \\\"core_variant\\\": \\\"E1R_REGIME_AWARE_V0_1\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0K_TRUE_COMPOSER_CALLSITE_TRACE.json",
        "line": 1032,
        "matched": [
          "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE"
        ],
        "text": "              \"text\": \"        \\\"regime_aware_logic\\\": \\\"UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0K_TRUE_COMPOSER_CALLSITE_TRACE.json",
        "line": 1040,
        "matched": [
          "E1R_REGIME_AWARE_V0_1"
        ],
        "text": "              \"text\": \"        \\\"e1r_v0_2_core_variant\\\": \\\"E1R_REGIME_AWARE_V0_1\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0K_TRUE_COMPOSER_CALLSITE_TRACE.json",
        "line": 1080,
        "matched": [
          "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE"
        ],
        "text": "              \"text\": \"        \\\"regime_aware_logic\\\": \\\"UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0K_TRUE_COMPOSER_CALLSITE_TRACE.json",
        "line": 1088,
        "matched": [
          "E1R_REGIME_AWARE_V0_1"
        ],
        "text": "              \"text\": \"        \\\"e1r_v0_2_core_variant\\\": \\\"E1R_REGIME_AWARE_V0_1\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0K_TRUE_COMPOSER_CALLSITE_TRACE.json",
        "line": 1128,
        "matched": [
          "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE"
        ],
        "text": "              \"text\": \"        \\\"regime_aware_logic\\\": \\\"UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0K_TRUE_COMPOSER_CALLSITE_TRACE.json",
        "line": 1136,
        "matched": [
          "E1R_REGIME_AWARE_V0_1"
        ],
        "text": "              \"text\": \"        \\\"e1r_v0_2_core_variant\\\": \\\"E1R_REGIME_AWARE_V0_1\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0K_TRUE_COMPOSER_CALLSITE_TRACE.json",
        "line": 1180,
        "matched": [
          "E1R_REGIME_AWARE_V0_1"
        ],
        "text": "              \"text\": \"        \\\"e1r_v0_2_core_variant\\\": \\\"E1R_REGIME_AWARE_V0_1\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0K_TRUE_COMPOSER_CALLSITE_TRACE.json",
        "line": 1222,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "            \"run_stateful_simulation\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0K_TRUE_COMPOSER_CALLSITE_TRACE.json",
        "line": 1247,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "              \"text\": \"def run_stateful_simulation(\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0K_TRUE_COMPOSER_CALLSITE_TRACE.json",
        "line": 1326,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "            \"run_stateful_simulation\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0K_TRUE_COMPOSER_CALLSITE_TRACE.json",
        "line": 1351,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "              \"text\": \"            _result = run_stateful_simulation(\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0K_TRUE_COMPOSER_CALLSITE_TRACE.json",
        "line": 1378,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "            \"run_stateful_simulation\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0K_TRUE_COMPOSER_CALLSITE_TRACE.json",
        "line": 1403,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "              \"text\": \"    # - Do not modify run_stateful_simulation().\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0K_TRUE_COMPOSER_CALLSITE_TRACE.json",
        "line": 1407,
        "matched": [
          "E1R_REGIME_AWARE_V0_1"
        ],
        "text": "              \"text\": \"    # - Do not modify E1R_REGIME_AWARE_V0_1.\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0K_TRUE_COMPOSER_CALLSITE_TRACE.json",
        "line": 1439,
        "matched": [
          "e1r_sidecar",
          "e1r_sidecar_sleeve"
        ],
        "text": "              \"text\": \"        from src.engine.e1r_sidecar_sleeve import (\""
      }
    ]
  },
  {
    "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0B_E1R_CORE_VARIANT_SOURCE_RECOVERY.json",
    "score": 10770,
    "hit_count": 158,
    "matched_terms": [
      "116.74",
      "116.7435999134756",
      "E1R_REGIME_AWARE_V0_1",
      "E1R_REGIME_AWARE_V0_2",
      "e1r_v0_2_backtest_summary",
      "market_entry_gate",
      "sidecar_active_by_regime"
    ],
    "sample_hits": [
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0B_E1R_CORE_VARIANT_SOURCE_RECOVERY.json",
        "line": 36,
        "matched": [
          "e1r_v0_2_backtest_summary"
        ],
        "text": "      \"exports/e1r_v0_2_backtest_summary.json\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0B_E1R_CORE_VARIANT_SOURCE_RECOVERY.json",
        "line": 96,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "    \"total_return_pct\": 116.7435999134756,"
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0B_E1R_CORE_VARIANT_SOURCE_RECOVERY.json",
        "line": 127,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "          \"value\": 116.7435999134756,"
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0B_E1R_CORE_VARIANT_SOURCE_RECOVERY.json",
        "line": 128,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "          \"target\": 116.7435999134756"
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0B_E1R_CORE_VARIANT_SOURCE_RECOVERY.json",
        "line": 157,
        "matched": [
          "e1r_v0_2_backtest_summary"
        ],
        "text": "        \"path\": \"$.inspection.exports/e1r_v0_2_backtest_summary.json.metrics\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0B_E1R_CORE_VARIANT_SOURCE_RECOVERY.json",
        "line": 170,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "          \"strategy_id\": \"E1R_REGIME_AWARE_V0_2\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0B_E1R_CORE_VARIANT_SOURCE_RECOVERY.json",
        "line": 171,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "          \"total_return_pct\": 116.7435999134756,"
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0B_E1R_CORE_VARIANT_SOURCE_RECOVERY.json",
        "line": 194,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "          \"value\": 116.7435999134756,"
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0B_E1R_CORE_VARIANT_SOURCE_RECOVERY.json",
        "line": 195,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "          \"target\": 116.7435999134756"
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0B_E1R_CORE_VARIANT_SOURCE_RECOVERY.json",
        "line": 238,
        "matched": [
          "sidecar_active_by_regime"
        ],
        "text": "          \"sidecar_active_by_regime\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0B_E1R_CORE_VARIANT_SOURCE_RECOVERY.json",
        "line": 249,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "          \"strategy_id\": \"E1R_REGIME_AWARE_V0_2\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0B_E1R_CORE_VARIANT_SOURCE_RECOVERY.json",
        "line": 250,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "          \"total_return_pct\": 116.7435999134756,"
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0B_E1R_CORE_VARIANT_SOURCE_RECOVERY.json",
        "line": 258,
        "matched": [
          "e1r_v0_2_backtest_summary"
        ],
        "text": "      \"file\": \"exports/e1r_v0_2_backtest_summary.json\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0B_E1R_CORE_VARIANT_SOURCE_RECOVERY.json",
        "line": 273,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "          \"value\": 116.7435999134756,"
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0B_E1R_CORE_VARIANT_SOURCE_RECOVERY.json",
        "line": 274,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "          \"target\": 116.7435999134756"
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0B_E1R_CORE_VARIANT_SOURCE_RECOVERY.json",
        "line": 314,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "          \"total_return_pct\": 116.7435999134756,"
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0B_E1R_CORE_VARIANT_SOURCE_RECOVERY.json",
        "line": 337,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "          \"value\": 116.7435999134756,"
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0B_E1R_CORE_VARIANT_SOURCE_RECOVERY.json",
        "line": 338,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "          \"target\": 116.7435999134756"
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0B_E1R_CORE_VARIANT_SOURCE_RECOVERY.json",
        "line": 378,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "          \"total_return_pct\": 116.7435999134756,"
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0B_E1R_CORE_VARIANT_SOURCE_RECOVERY.json",
        "line": 401,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "          \"value\": 116.7435999134756,"
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0B_E1R_CORE_VARIANT_SOURCE_RECOVERY.json",
        "line": 402,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "          \"target\": 116.7435999134756"
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0B_E1R_CORE_VARIANT_SOURCE_RECOVERY.json",
        "line": 442,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "          \"total_return_pct\": 116.7435999134756,"
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0B_E1R_CORE_VARIANT_SOURCE_RECOVERY.json",
        "line": 465,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "          \"value\": 116.7435999134756,"
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0B_E1R_CORE_VARIANT_SOURCE_RECOVERY.json",
        "line": 466,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "          \"target\": 116.7435999134756"
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0B_E1R_CORE_VARIANT_SOURCE_RECOVERY.json",
        "line": 506,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "          \"total_return_pct\": 116.7435999134756,"
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0B_E1R_CORE_VARIANT_SOURCE_RECOVERY.json",
        "line": 529,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "          \"value\": 116.7435999134756,"
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0B_E1R_CORE_VARIANT_SOURCE_RECOVERY.json",
        "line": 530,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "          \"target\": 116.7435999134756"
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0B_E1R_CORE_VARIANT_SOURCE_RECOVERY.json",
        "line": 570,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "          \"total_return_pct\": 116.7435999134756,"
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0B_E1R_CORE_VARIANT_SOURCE_RECOVERY.json",
        "line": 593,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "          \"value\": 116.7435999134756,"
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0B_E1R_CORE_VARIANT_SOURCE_RECOVERY.json",
        "line": 594,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "          \"target\": 116.7435999134756"
      }
    ]
  },
  {
    "path": "docs/research/E1R_4C2C4E_D1_UPTREND_PROVIDER_ENTRYPOINT_AUDIT.json",
    "score": 9920,
    "hit_count": 345,
    "matched_terms": [
      "D3_RISK_OFF_PLUS_SHOCK_GATE",
      "e1r_composer",
      "e1r_sidecar",
      "e1r_sidecar_sleeve",
      "market_gate_enabled",
      "market_shock_daily_return",
      "market_shock_gate_enabled",
      "risk_off_below_spx_ma50",
      "run_stateful_simulation"
    ],
    "sample_hits": [
      {
        "path": "docs/research/E1R_4C2C4E_D1_UPTREND_PROVIDER_ENTRYPOINT_AUDIT.json",
        "line": 44,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "    \"function\": \"run_stateful_simulation\","
      },
      {
        "path": "docs/research/E1R_4C2C4E_D1_UPTREND_PROVIDER_ENTRYPOINT_AUDIT.json",
        "line": 917,
        "matched": [
          "market_gate_enabled"
        ],
        "text": "            \"text\": \"    market_gate_enabled = bool(a.get(\\\"market_gate_enabled\\\", True))\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_D1_UPTREND_PROVIDER_ENTRYPOINT_AUDIT.json",
        "line": 987,
        "matched": [
          "market_gate_enabled"
        ],
        "text": "            \"text\": \"    market_gate_enabled = bool(a.get(\\\"market_gate_enabled\\\", True))\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_D1_UPTREND_PROVIDER_ENTRYPOINT_AUDIT.json",
        "line": 991,
        "matched": [
          "risk_off_below_spx_ma50"
        ],
        "text": "            \"text\": \"    risk_off_below_spx_ma50 = bool(a.get(\\\"risk_off_below_spx_ma50\\\", True))\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_D1_UPTREND_PROVIDER_ENTRYPOINT_AUDIT.json",
        "line": 1061,
        "matched": [
          "market_gate_enabled"
        ],
        "text": "            \"text\": \"    market_gate_enabled = bool(a.get(\\\"market_gate_enabled\\\", True))\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_D1_UPTREND_PROVIDER_ENTRYPOINT_AUDIT.json",
        "line": 1065,
        "matched": [
          "risk_off_below_spx_ma50"
        ],
        "text": "            \"text\": \"    risk_off_below_spx_ma50 = bool(a.get(\\\"risk_off_below_spx_ma50\\\", True))\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_D1_UPTREND_PROVIDER_ENTRYPOINT_AUDIT.json",
        "line": 1111,
        "matched": [
          "market_gate_enabled"
        ],
        "text": "            \"text\": \"    market_gate_enabled = bool(a.get(\\\"market_gate_enabled\\\", True))\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_D1_UPTREND_PROVIDER_ENTRYPOINT_AUDIT.json",
        "line": 1115,
        "matched": [
          "risk_off_below_spx_ma50"
        ],
        "text": "            \"text\": \"    risk_off_below_spx_ma50 = bool(a.get(\\\"risk_off_below_spx_ma50\\\", True))\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_D1_UPTREND_PROVIDER_ENTRYPOINT_AUDIT.json",
        "line": 1185,
        "matched": [
          "market_gate_enabled"
        ],
        "text": "            \"text\": \"    market_gate_enabled = bool(a.get(\\\"market_gate_enabled\\\", True))\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_D1_UPTREND_PROVIDER_ENTRYPOINT_AUDIT.json",
        "line": 1189,
        "matched": [
          "risk_off_below_spx_ma50"
        ],
        "text": "            \"text\": \"    risk_off_below_spx_ma50 = bool(a.get(\\\"risk_off_below_spx_ma50\\\", True))\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_D1_UPTREND_PROVIDER_ENTRYPOINT_AUDIT.json",
        "line": 1235,
        "matched": [
          "market_gate_enabled"
        ],
        "text": "        \"text\": \"market_gate_enabled = bool(a.get(\\\"market_gate_enabled\\\", True))\","
      },
      {
        "path": "docs/research/E1R_4C2C4E_D1_UPTREND_PROVIDER_ENTRYPOINT_AUDIT.json",
        "line": 1259,
        "matched": [
          "market_gate_enabled"
        ],
        "text": "            \"text\": \"    market_gate_enabled = bool(a.get(\\\"market_gate_enabled\\\", True))\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_D1_UPTREND_PROVIDER_ENTRYPOINT_AUDIT.json",
        "line": 1263,
        "matched": [
          "risk_off_below_spx_ma50"
        ],
        "text": "            \"text\": \"    risk_off_below_spx_ma50 = bool(a.get(\\\"risk_off_below_spx_ma50\\\", True))\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_D1_UPTREND_PROVIDER_ENTRYPOINT_AUDIT.json",
        "line": 1329,
        "matched": [
          "market_gate_enabled"
        ],
        "text": "            \"text\": \"    market_gate_enabled = bool(a.get(\\\"market_gate_enabled\\\", True))\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_D1_UPTREND_PROVIDER_ENTRYPOINT_AUDIT.json",
        "line": 1333,
        "matched": [
          "risk_off_below_spx_ma50"
        ],
        "text": "            \"text\": \"    risk_off_below_spx_ma50 = bool(a.get(\\\"risk_off_below_spx_ma50\\\", True))\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_D1_UPTREND_PROVIDER_ENTRYPOINT_AUDIT.json",
        "line": 1395,
        "matched": [
          "market_gate_enabled"
        ],
        "text": "            \"text\": \"    market_gate_enabled = bool(a.get(\\\"market_gate_enabled\\\", True))\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_D1_UPTREND_PROVIDER_ENTRYPOINT_AUDIT.json",
        "line": 1399,
        "matched": [
          "risk_off_below_spx_ma50"
        ],
        "text": "            \"text\": \"    risk_off_below_spx_ma50 = bool(a.get(\\\"risk_off_below_spx_ma50\\\", True))\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_D1_UPTREND_PROVIDER_ENTRYPOINT_AUDIT.json",
        "line": 1473,
        "matched": [
          "risk_off_below_spx_ma50"
        ],
        "text": "            \"text\": \"    risk_off_below_spx_ma50 = bool(a.get(\\\"risk_off_below_spx_ma50\\\", True))\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_D1_UPTREND_PROVIDER_ENTRYPOINT_AUDIT.json",
        "line": 1685,
        "matched": [
          "market_shock_gate_enabled"
        ],
        "text": "            \"text\": \"    market_shock_gate_enabled = bool(a.get(\\\"market_shock_gate_enabled\\\", True))\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_D1_UPTREND_PROVIDER_ENTRYPOINT_AUDIT.json",
        "line": 1689,
        "matched": [
          "market_shock_daily_return"
        ],
        "text": "            \"text\": \"    market_shock_daily_return = float(a.get(\\\"market_shock_daily_return\\\", -0.02))\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_D1_UPTREND_PROVIDER_ENTRYPOINT_AUDIT.json",
        "line": 1759,
        "matched": [
          "market_shock_gate_enabled"
        ],
        "text": "            \"text\": \"    market_shock_gate_enabled = bool(a.get(\\\"market_shock_gate_enabled\\\", True))\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_D1_UPTREND_PROVIDER_ENTRYPOINT_AUDIT.json",
        "line": 1763,
        "matched": [
          "market_shock_daily_return"
        ],
        "text": "            \"text\": \"    market_shock_daily_return = float(a.get(\\\"market_shock_daily_return\\\", -0.02))\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_D1_UPTREND_PROVIDER_ENTRYPOINT_AUDIT.json",
        "line": 1817,
        "matched": [
          "market_shock_gate_enabled"
        ],
        "text": "            \"text\": \"    market_shock_gate_enabled = bool(a.get(\\\"market_shock_gate_enabled\\\", True))\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_D1_UPTREND_PROVIDER_ENTRYPOINT_AUDIT.json",
        "line": 1821,
        "matched": [
          "market_shock_daily_return"
        ],
        "text": "            \"text\": \"    market_shock_daily_return = float(a.get(\\\"market_shock_daily_return\\\", -0.02))\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_D1_UPTREND_PROVIDER_ENTRYPOINT_AUDIT.json",
        "line": 1891,
        "matched": [
          "market_shock_gate_enabled"
        ],
        "text": "            \"text\": \"    market_shock_gate_enabled = bool(a.get(\\\"market_shock_gate_enabled\\\", True))\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_D1_UPTREND_PROVIDER_ENTRYPOINT_AUDIT.json",
        "line": 1895,
        "matched": [
          "market_shock_daily_return"
        ],
        "text": "            \"text\": \"    market_shock_daily_return = float(a.get(\\\"market_shock_daily_return\\\", -0.02))\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_D1_UPTREND_PROVIDER_ENTRYPOINT_AUDIT.json",
        "line": 1965,
        "matched": [
          "market_shock_gate_enabled"
        ],
        "text": "            \"text\": \"    market_shock_gate_enabled = bool(a.get(\\\"market_shock_gate_enabled\\\", True))\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_D1_UPTREND_PROVIDER_ENTRYPOINT_AUDIT.json",
        "line": 1969,
        "matched": [
          "market_shock_daily_return"
        ],
        "text": "            \"text\": \"    market_shock_daily_return = float(a.get(\\\"market_shock_daily_return\\\", -0.02))\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_D1_UPTREND_PROVIDER_ENTRYPOINT_AUDIT.json",
        "line": 2075,
        "matched": [
          "market_gate_enabled"
        ],
        "text": "            \"text\": \"        \\\"D1_NO_MARKET_GATE\\\" if not market_gate_enabled else\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_D1_UPTREND_PROVIDER_ENTRYPOINT_AUDIT.json",
        "line": 2079,
        "matched": [
          "market_shock_gate_enabled"
        ],
        "text": "            \"text\": \"        \\\"D2_RISK_OFF_GATE\\\" if not market_shock_gate_enabled else\""
      }
    ]
  },
  {
    "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C3_BACKTEST_GENERATOR_CANONICAL_EXPORT_PLAN.json",
    "score": 9150,
    "hit_count": 187,
    "matched_terms": [
      "116.74",
      "116.7435999134756",
      "E1R_REGIME_AWARE_V0_1",
      "E1R_REGIME_AWARE_V0_2",
      "e1r_composer",
      "e1r_sidecar",
      "e1r_sidecar_sleeve",
      "e1r_v0_2_backtest_summary",
      "market_entry_gate",
      "market_gate_enabled",
      "market_shock_daily_return",
      "market_shock_gate_enabled",
      "run_stateful_simulation",
      "sidecar_active_by_regime"
    ],
    "sample_hits": [
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C3_BACKTEST_GENERATOR_CANONICAL_EXPORT_PLAN.json",
        "line": 162,
        "matched": [
          "market_entry_gate"
        ],
        "text": "        \"market_entry_gate\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C3_BACKTEST_GENERATOR_CANONICAL_EXPORT_PLAN.json",
        "line": 225,
        "matched": [
          "e1r_v0_2_backtest_summary"
        ],
        "text": "    \"exports/e1r_v0_2_backtest_summary.json\": {"
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C3_BACKTEST_GENERATOR_CANONICAL_EXPORT_PLAN.json",
        "line": 241,
        "matched": [
          "sidecar_active_by_regime"
        ],
        "text": "        \"sidecar_active_by_regime\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C3_BACKTEST_GENERATOR_CANONICAL_EXPORT_PLAN.json",
        "line": 251,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "      \"total_return_pct\": 116.7435999134756,"
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C3_BACKTEST_GENERATOR_CANONICAL_EXPORT_PLAN.json",
        "line": 256,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "      \"strategy_id\": \"E1R_REGIME_AWARE_V0_2\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C3_BACKTEST_GENERATOR_CANONICAL_EXPORT_PLAN.json",
        "line": 257,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "      \"variant\": \"E1R_REGIME_AWARE_V0_2\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C3_BACKTEST_GENERATOR_CANONICAL_EXPORT_PLAN.json",
        "line": 348,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "      \"variant\": \"E1R_REGIME_AWARE_V0_2\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C3_BACKTEST_GENERATOR_CANONICAL_EXPORT_PLAN.json",
        "line": 360,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C3_BACKTEST_GENERATOR_CANONICAL_EXPORT_PLAN.json",
        "line": 464,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "            \"E1R_REGIME_AWARE_V0_2\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C3_BACKTEST_GENERATOR_CANONICAL_EXPORT_PLAN.json",
        "line": 466,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "          \"text\": \"    strategy_id = status.get(\\\"strategy_id\\\", \\\"E1R_REGIME_AWARE_V0_2\\\")\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C3_BACKTEST_GENERATOR_CANONICAL_EXPORT_PLAN.json",
        "line": 534,
        "matched": [
          "E1R_REGIME_AWARE_V0_1"
        ],
        "text": "            \"E1R_REGIME_AWARE_V0_1\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C3_BACKTEST_GENERATOR_CANONICAL_EXPORT_PLAN.json",
        "line": 536,
        "matched": [
          "E1R_REGIME_AWARE_V0_1"
        ],
        "text": "          \"text\": \"            \\\"strategy_id\\\": core.get(\\\"strategy_id\\\", \\\"E1R_REGIME_AWARE_V0_1\\\"),\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C3_BACKTEST_GENERATOR_CANONICAL_EXPORT_PLAN.json",
        "line": 793,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "            \"E1R_REGIME_AWARE_V0_2\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C3_BACKTEST_GENERATOR_CANONICAL_EXPORT_PLAN.json",
        "line": 795,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "          \"text\": \"STRATEGY_ID = \\\"E1R_REGIME_AWARE_V0_2\\\"\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C3_BACKTEST_GENERATOR_CANONICAL_EXPORT_PLAN.json",
        "line": 1277,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "            \"E1R_REGIME_AWARE_V0_2\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C3_BACKTEST_GENERATOR_CANONICAL_EXPORT_PLAN.json",
        "line": 1279,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "          \"text\": \"        \\\"strategy_id\\\": \\\"E1R_REGIME_AWARE_V0_2\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C3_BACKTEST_GENERATOR_CANONICAL_EXPORT_PLAN.json",
        "line": 1436,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "            \"E1R_REGIME_AWARE_V0_2\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C3_BACKTEST_GENERATOR_CANONICAL_EXPORT_PLAN.json",
        "line": 1438,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "          \"text\": \"STRATEGY_ID = \\\"E1R_REGIME_AWARE_V0_2\\\"\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C3_BACKTEST_GENERATOR_CANONICAL_EXPORT_PLAN.json",
        "line": 1814,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "            \"E1R_REGIME_AWARE_V0_2\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C3_BACKTEST_GENERATOR_CANONICAL_EXPORT_PLAN.json",
        "line": 1816,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "          \"text\": \"STRATEGY_ID = \\\"E1R_REGIME_AWARE_V0_2\\\"\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C3_BACKTEST_GENERATOR_CANONICAL_EXPORT_PLAN.json",
        "line": 2169,
        "matched": [
          "E1R_REGIME_AWARE_V0_1"
        ],
        "text": "            \"E1R_REGIME_AWARE_V0_1\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C3_BACKTEST_GENERATOR_CANONICAL_EXPORT_PLAN.json",
        "line": 2171,
        "matched": [
          "E1R_REGIME_AWARE_V0_1"
        ],
        "text": "          \"text\": \"    v1 = extract_variant(variants, \\\"E1R_REGIME_AWARE_V0_1\\\")\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C3_BACKTEST_GENERATOR_CANONICAL_EXPORT_PLAN.json",
        "line": 2176,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "            \"E1R_REGIME_AWARE_V0_2\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C3_BACKTEST_GENERATOR_CANONICAL_EXPORT_PLAN.json",
        "line": 2178,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "          \"text\": \"    v2 = extract_variant(variants, \\\"E1R_REGIME_AWARE_V0_2\\\")\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C3_BACKTEST_GENERATOR_CANONICAL_EXPORT_PLAN.json",
        "line": 2221,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "            \"E1R_REGIME_AWARE_V0_2\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C3_BACKTEST_GENERATOR_CANONICAL_EXPORT_PLAN.json",
        "line": 2223,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "          \"text\": \"        \\\"strategy_id\\\": \\\"E1R_REGIME_AWARE_V0_2\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C3_BACKTEST_GENERATOR_CANONICAL_EXPORT_PLAN.json",
        "line": 2228,
        "matched": [
          "E1R_REGIME_AWARE_V0_1"
        ],
        "text": "            \"E1R_REGIME_AWARE_V0_1\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C3_BACKTEST_GENERATOR_CANONICAL_EXPORT_PLAN.json",
        "line": 2230,
        "matched": [
          "E1R_REGIME_AWARE_V0_1"
        ],
        "text": "          \"text\": \"            \\\"strategy_id\\\": \\\"E1R_REGIME_AWARE_V0_1\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C3_BACKTEST_GENERATOR_CANONICAL_EXPORT_PLAN.json",
        "line": 2235,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "            \"E1R_REGIME_AWARE_V0_2\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C3_BACKTEST_GENERATOR_CANONICAL_EXPORT_PLAN.json",
        "line": 2237,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "          \"text\": \"            \\\"strategy_id\\\": \\\"E1R_REGIME_AWARE_V0_2\\\",\""
      }
    ]
  },
  {
    "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0B_E1R_CORE_VARIANT_SOURCE_RECOVERY.md",
    "score": 8550,
    "hit_count": 120,
    "matched_terms": [
      "116.74",
      "116.7435999134756",
      "E1R_REGIME_AWARE_V0_2",
      "e1r_v0_2_backtest_summary",
      "market_entry_gate",
      "sidecar_active_by_regime"
    ],
    "sample_hits": [
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0B_E1R_CORE_VARIANT_SOURCE_RECOVERY.md",
        "line": 43,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "        \"value\": 116.7435999134756,"
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0B_E1R_CORE_VARIANT_SOURCE_RECOVERY.md",
        "line": 44,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "        \"target\": 116.7435999134756"
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0B_E1R_CORE_VARIANT_SOURCE_RECOVERY.md",
        "line": 73,
        "matched": [
          "e1r_v0_2_backtest_summary"
        ],
        "text": "      \"path\": \"$.inspection.exports/e1r_v0_2_backtest_summary.json.metrics\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0B_E1R_CORE_VARIANT_SOURCE_RECOVERY.md",
        "line": 86,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0B_E1R_CORE_VARIANT_SOURCE_RECOVERY.md",
        "line": 87,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "        \"total_return_pct\": 116.7435999134756,"
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0B_E1R_CORE_VARIANT_SOURCE_RECOVERY.md",
        "line": 110,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "        \"value\": 116.7435999134756,"
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0B_E1R_CORE_VARIANT_SOURCE_RECOVERY.md",
        "line": 111,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "        \"target\": 116.7435999134756"
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0B_E1R_CORE_VARIANT_SOURCE_RECOVERY.md",
        "line": 154,
        "matched": [
          "sidecar_active_by_regime"
        ],
        "text": "        \"sidecar_active_by_regime\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0B_E1R_CORE_VARIANT_SOURCE_RECOVERY.md",
        "line": 165,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0B_E1R_CORE_VARIANT_SOURCE_RECOVERY.md",
        "line": 166,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "        \"total_return_pct\": 116.7435999134756,"
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0B_E1R_CORE_VARIANT_SOURCE_RECOVERY.md",
        "line": 174,
        "matched": [
          "e1r_v0_2_backtest_summary"
        ],
        "text": "    \"file\": \"exports/e1r_v0_2_backtest_summary.json\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0B_E1R_CORE_VARIANT_SOURCE_RECOVERY.md",
        "line": 189,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "        \"value\": 116.7435999134756,"
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0B_E1R_CORE_VARIANT_SOURCE_RECOVERY.md",
        "line": 190,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "        \"target\": 116.7435999134756"
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0B_E1R_CORE_VARIANT_SOURCE_RECOVERY.md",
        "line": 230,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "        \"total_return_pct\": 116.7435999134756,"
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0B_E1R_CORE_VARIANT_SOURCE_RECOVERY.md",
        "line": 253,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "        \"value\": 116.7435999134756,"
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0B_E1R_CORE_VARIANT_SOURCE_RECOVERY.md",
        "line": 254,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "        \"target\": 116.7435999134756"
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0B_E1R_CORE_VARIANT_SOURCE_RECOVERY.md",
        "line": 294,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "        \"total_return_pct\": 116.7435999134756,"
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0B_E1R_CORE_VARIANT_SOURCE_RECOVERY.md",
        "line": 317,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "        \"value\": 116.7435999134756,"
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0B_E1R_CORE_VARIANT_SOURCE_RECOVERY.md",
        "line": 318,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "        \"target\": 116.7435999134756"
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0B_E1R_CORE_VARIANT_SOURCE_RECOVERY.md",
        "line": 358,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "        \"total_return_pct\": 116.7435999134756,"
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0B_E1R_CORE_VARIANT_SOURCE_RECOVERY.md",
        "line": 381,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "        \"value\": 116.7435999134756,"
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0B_E1R_CORE_VARIANT_SOURCE_RECOVERY.md",
        "line": 382,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "        \"target\": 116.7435999134756"
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0B_E1R_CORE_VARIANT_SOURCE_RECOVERY.md",
        "line": 422,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "        \"total_return_pct\": 116.7435999134756,"
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0B_E1R_CORE_VARIANT_SOURCE_RECOVERY.md",
        "line": 445,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "        \"value\": 116.7435999134756,"
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0B_E1R_CORE_VARIANT_SOURCE_RECOVERY.md",
        "line": 446,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "        \"target\": 116.7435999134756"
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0B_E1R_CORE_VARIANT_SOURCE_RECOVERY.md",
        "line": 486,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "        \"total_return_pct\": 116.7435999134756,"
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0B_E1R_CORE_VARIANT_SOURCE_RECOVERY.md",
        "line": 509,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "        \"value\": 116.7435999134756,"
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0B_E1R_CORE_VARIANT_SOURCE_RECOVERY.md",
        "line": 510,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "        \"target\": 116.7435999134756"
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0B_E1R_CORE_VARIANT_SOURCE_RECOVERY.md",
        "line": 550,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "        \"total_return_pct\": 116.7435999134756,"
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0B_E1R_CORE_VARIANT_SOURCE_RECOVERY.md",
        "line": 572,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "        \"value\": 116.7435999134756,"
      }
    ]
  },
  {
    "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0I_COMPOSER_INPUT_CANDIDATES.json",
    "score": 8020,
    "hit_count": 125,
    "matched_terms": [
      "116.74",
      "116.7435999134756",
      "E1R_REGIME_AWARE_V0_2",
      "e1r_composer",
      "e1r_sidecar",
      "e1r_sidecar_sleeve",
      "e1r_v0_2_backtest_summary",
      "market_entry_gate",
      "sidecar_active_by_regime"
    ],
    "sample_hits": [
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0I_COMPOSER_INPUT_CANDIDATES.json",
        "line": 4,
        "matched": [
          "e1r_composer"
        ],
        "text": "  \"status\": \"E1R_COMPOSER_INPUT_CANDIDATES_AUDIT_COMPLETE_NO_INVOCATION\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0I_COMPOSER_INPUT_CANDIDATES.json",
        "line": 73,
        "matched": [
          "market_entry_gate"
        ],
        "text": "          \"market_entry_gate\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0I_COMPOSER_INPUT_CANDIDATES.json",
        "line": 163,
        "matched": [
          "market_entry_gate"
        ],
        "text": "          \"market_entry_gate\": {"
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0I_COMPOSER_INPUT_CANDIDATES.json",
        "line": 663,
        "matched": [
          "market_entry_gate"
        ],
        "text": "          \"market_entry_gate\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0I_COMPOSER_INPUT_CANDIDATES.json",
        "line": 749,
        "matched": [
          "market_entry_gate"
        ],
        "text": "          \"market_entry_gate\": {"
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0I_COMPOSER_INPUT_CANDIDATES.json",
        "line": 1088,
        "matched": [
          "market_entry_gate"
        ],
        "text": "          \"market_entry_gate\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0I_COMPOSER_INPUT_CANDIDATES.json",
        "line": 1174,
        "matched": [
          "market_entry_gate"
        ],
        "text": "          \"market_entry_gate\": {"
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0I_COMPOSER_INPUT_CANDIDATES.json",
        "line": 1600,
        "matched": [
          "market_entry_gate"
        ],
        "text": "          \"market_entry_gate\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0I_COMPOSER_INPUT_CANDIDATES.json",
        "line": 1686,
        "matched": [
          "market_entry_gate"
        ],
        "text": "          \"market_entry_gate\": {"
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0I_COMPOSER_INPUT_CANDIDATES.json",
        "line": 2025,
        "matched": [
          "market_entry_gate"
        ],
        "text": "          \"market_entry_gate\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0I_COMPOSER_INPUT_CANDIDATES.json",
        "line": 2111,
        "matched": [
          "market_entry_gate"
        ],
        "text": "          \"market_entry_gate\": {"
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0I_COMPOSER_INPUT_CANDIDATES.json",
        "line": 2539,
        "matched": [
          "market_entry_gate"
        ],
        "text": "          \"market_entry_gate\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0I_COMPOSER_INPUT_CANDIDATES.json",
        "line": 2627,
        "matched": [
          "market_entry_gate"
        ],
        "text": "          \"market_entry_gate\": {"
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0I_COMPOSER_INPUT_CANDIDATES.json",
        "line": 3215,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "          \"total_return_pct\": 116.7435999134756,"
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0I_COMPOSER_INPUT_CANDIDATES.json",
        "line": 3245,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "          \"total_return_pct\": 116.7435999134756,"
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0I_COMPOSER_INPUT_CANDIDATES.json",
        "line": 3264,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "          \"total_return_pct\": 116.7435999134756,"
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0I_COMPOSER_INPUT_CANDIDATES.json",
        "line": 3294,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "          \"total_return_pct\": 116.7435999134756,"
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0I_COMPOSER_INPUT_CANDIDATES.json",
        "line": 3306,
        "matched": [
          "e1r_v0_2_backtest_summary"
        ],
        "text": "      \"json_path\": \"$.inspection.exports/e1r_v0_2_backtest_summary.json.metrics\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0I_COMPOSER_INPUT_CANDIDATES.json",
        "line": 3313,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "          \"total_return_pct\": 116.7435999134756,"
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0I_COMPOSER_INPUT_CANDIDATES.json",
        "line": 3344,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "          \"strategy_id\": \"E1R_REGIME_AWARE_V0_2\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0I_COMPOSER_INPUT_CANDIDATES.json",
        "line": 3345,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "          \"total_return_pct\": 116.7435999134756,"
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0I_COMPOSER_INPUT_CANDIDATES.json",
        "line": 3356,
        "matched": [
          "e1r_v0_2_backtest_summary"
        ],
        "text": "      \"source_file\": \"exports/e1r_v0_2_backtest_summary.json\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0I_COMPOSER_INPUT_CANDIDATES.json",
        "line": 3364,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "          \"total_return_pct\": 116.7435999134756,"
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0I_COMPOSER_INPUT_CANDIDATES.json",
        "line": 3396,
        "matched": [
          "sidecar_active_by_regime"
        ],
        "text": "          \"sidecar_active_by_regime\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0I_COMPOSER_INPUT_CANDIDATES.json",
        "line": 3407,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "          \"strategy_id\": \"E1R_REGIME_AWARE_V0_2\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0I_COMPOSER_INPUT_CANDIDATES.json",
        "line": 3408,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "          \"total_return_pct\": 116.7435999134756,"
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0I_COMPOSER_INPUT_CANDIDATES.json",
        "line": 3417,
        "matched": [
          "sidecar_active_by_regime"
        ],
        "text": "          \"sidecar_active_by_regime\": {"
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0I_COMPOSER_INPUT_CANDIDATES.json",
        "line": 3648,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "          \"total_return_pct\": 116.7435999134756,"
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0I_COMPOSER_INPUT_CANDIDATES.json",
        "line": 3677,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "          \"total_return_pct\": 116.7435999134756,"
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0I_COMPOSER_INPUT_CANDIDATES.json",
        "line": 3740,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "            \"target\": 116.7435999134756"
      }
    ]
  },
  {
    "path": "docs/research/E1R_4C2C4E_B2_BACKTEST_ASSUMPTIONS_CONTRACT_AUDIT.json",
    "score": 7420,
    "hit_count": 313,
    "matched_terms": [
      "E1R_REGIME_AWARE_V0_1",
      "E1R_REGIME_AWARE_V0_2",
      "e1r_composer",
      "e1r_sidecar",
      "e1r_sidecar_sleeve",
      "e1r_v0_2_backtest_summary",
      "market_entry_gate",
      "market_gate_enabled",
      "market_shock_daily_return",
      "market_shock_gate_enabled",
      "risk_off_below_spx_ma50",
      "run_stateful_simulation"
    ],
    "sample_hits": [
      {
        "path": "docs/research/E1R_4C2C4E_B2_BACKTEST_ASSUMPTIONS_CONTRACT_AUDIT.json",
        "line": 17,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "    \"function\": \"run_stateful_simulation\","
      },
      {
        "path": "docs/research/E1R_4C2C4E_B2_BACKTEST_ASSUMPTIONS_CONTRACT_AUDIT.json",
        "line": 376,
        "matched": [
          "market_gate_enabled"
        ],
        "text": "      \"market_gate_enabled\": {"
      },
      {
        "path": "docs/research/E1R_4C2C4E_B2_BACKTEST_ASSUMPTIONS_CONTRACT_AUDIT.json",
        "line": 392,
        "matched": [
          "market_gate_enabled"
        ],
        "text": "            \"text\": \"market_gate_enabled = bool(a.get(\\\"market_gate_enabled\\\", True))\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_B2_BACKTEST_ASSUMPTIONS_CONTRACT_AUDIT.json",
        "line": 397,
        "matched": [
          "market_shock_daily_return"
        ],
        "text": "      \"market_shock_daily_return\": {"
      },
      {
        "path": "docs/research/E1R_4C2C4E_B2_BACKTEST_ASSUMPTIONS_CONTRACT_AUDIT.json",
        "line": 413,
        "matched": [
          "market_shock_daily_return"
        ],
        "text": "            \"text\": \"market_shock_daily_return = float(a.get(\\\"market_shock_daily_return\\\", -0.02))\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_B2_BACKTEST_ASSUMPTIONS_CONTRACT_AUDIT.json",
        "line": 418,
        "matched": [
          "market_shock_gate_enabled"
        ],
        "text": "      \"market_shock_gate_enabled\": {"
      },
      {
        "path": "docs/research/E1R_4C2C4E_B2_BACKTEST_ASSUMPTIONS_CONTRACT_AUDIT.json",
        "line": 434,
        "matched": [
          "market_shock_gate_enabled"
        ],
        "text": "            \"text\": \"market_shock_gate_enabled = bool(a.get(\\\"market_shock_gate_enabled\\\", True))\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_B2_BACKTEST_ASSUMPTIONS_CONTRACT_AUDIT.json",
        "line": 828,
        "matched": [
          "risk_off_below_spx_ma50"
        ],
        "text": "      \"risk_off_below_spx_ma50\": {"
      },
      {
        "path": "docs/research/E1R_4C2C4E_B2_BACKTEST_ASSUMPTIONS_CONTRACT_AUDIT.json",
        "line": 844,
        "matched": [
          "risk_off_below_spx_ma50"
        ],
        "text": "            \"text\": \"risk_off_below_spx_ma50 = bool(a.get(\\\"risk_off_below_spx_ma50\\\", True))\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_B2_BACKTEST_ASSUMPTIONS_CONTRACT_AUDIT.json",
        "line": 942,
        "matched": [
          "e1r_sidecar",
          "e1r_sidecar_sleeve"
        ],
        "text": "          \"text\": \"    \\\"build_e1r_sidecar_sleeve\\\",\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_B2_BACKTEST_ASSUMPTIONS_CONTRACT_AUDIT.json",
        "line": 950,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "          \"text\": \"    \\\"run_stateful_simulation\\\",\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_B2_BACKTEST_ASSUMPTIONS_CONTRACT_AUDIT.json",
        "line": 954,
        "matched": [
          "e1r_v0_2_backtest_summary"
        ],
        "text": "          \"text\": \"    \\\"e1r_v0_2_backtest_summary.json\\\",\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_B2_BACKTEST_ASSUMPTIONS_CONTRACT_AUDIT.json",
        "line": 962,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "          \"text\": \"    \\\"E1R_REGIME_AWARE_V0_2\\\",\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_B2_BACKTEST_ASSUMPTIONS_CONTRACT_AUDIT.json",
        "line": 1048,
        "matched": [
          "e1r_v0_2_backtest_summary"
        ],
        "text": "          \"text\": \"    if \\\"e1r_v0_2_backtest_equity_curve.json\\\" in generator_text and \\\"e1r_v0_2_backtest_summary.json\\\" in generator_text:\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_B2_BACKTEST_ASSUMPTIONS_CONTRACT_AUDIT.json",
        "line": 1072,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "          \"text\": \"    next_actions.append(\\\"If composer returns only metrics plus diagnostic rows, inspect upstream run_stateful_simulation / run_strategy_variant_comparison return object.\\\")\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_B2_BACKTEST_ASSUMPTIONS_CONTRACT_AUDIT.json",
        "line": 1194,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "          \"text\": \"    \\\"run_stateful_simulation\\\",\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_B2_BACKTEST_ASSUMPTIONS_CONTRACT_AUDIT.json",
        "line": 1218,
        "matched": [
          "market_shock_daily_return"
        ],
        "text": "          \"text\": \"    \\\"market_shock_daily_return\\\",\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_B2_BACKTEST_ASSUMPTIONS_CONTRACT_AUDIT.json",
        "line": 1226,
        "matched": [
          "market_shock_gate_enabled"
        ],
        "text": "          \"text\": \"    \\\"market_shock_gate_enabled\\\",\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_B2_BACKTEST_ASSUMPTIONS_CONTRACT_AUDIT.json",
        "line": 1316,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "          \"text\": \"        if isinstance(node, ast.FunctionDef) and node.name == \\\"run_stateful_simulation\\\":\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_B2_BACKTEST_ASSUMPTIONS_CONTRACT_AUDIT.json",
        "line": 1336,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "          \"text\": \"        return {\\\"error\\\": \\\"run_stateful_simulation not found\\\"}\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_B2_BACKTEST_ASSUMPTIONS_CONTRACT_AUDIT.json",
        "line": 1418,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "          \"text\": \"        if isinstance(node, ast.FunctionDef) and node.name == \\\"run_stateful_simulation\\\":\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_B2_BACKTEST_ASSUMPTIONS_CONTRACT_AUDIT.json",
        "line": 1438,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "          \"text\": \"        return {\\\"error\\\": \\\"run_stateful_simulation not found\\\"}\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_B2_BACKTEST_ASSUMPTIONS_CONTRACT_AUDIT.json",
        "line": 1560,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "          \"text\": \"        \\\"function\\\": \\\"run_stateful_simulation\\\",\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_B2_BACKTEST_ASSUMPTIONS_CONTRACT_AUDIT.json",
        "line": 1596,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "          \"text\": \"        if \\\"run_stateful_simulation\\\" not in text:\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_B2_BACKTEST_ASSUMPTIONS_CONTRACT_AUDIT.json",
        "line": 1612,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "          \"text\": \"            if \\\"run_stateful_simulation\\\" in line:\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_B2_BACKTEST_ASSUMPTIONS_CONTRACT_AUDIT.json",
        "line": 1682,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "          \"text\": \"        if \\\"run_stateful_simulation\\\" not in text:\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_B2_BACKTEST_ASSUMPTIONS_CONTRACT_AUDIT.json",
        "line": 1698,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "          \"text\": \"            if \\\"run_stateful_simulation\\\" in line:\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_B2_BACKTEST_ASSUMPTIONS_CONTRACT_AUDIT.json",
        "line": 1788,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "          \"text\": \"        if \\\"run_stateful_simulation\\\" not in text:\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_B2_BACKTEST_ASSUMPTIONS_CONTRACT_AUDIT.json",
        "line": 1804,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "          \"text\": \"            if \\\"run_stateful_simulation\\\" in line:\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_B2_BACKTEST_ASSUMPTIONS_CONTRACT_AUDIT.json",
        "line": 1926,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "          \"text\": \"    run_info = funcs.get(\\\"run_stateful_simulation\\\", {})\""
      }
    ]
  },
  {
    "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2A_ENGINE_ENTRYPOINT_REPORT.json",
    "score": 6200,
    "hit_count": 168,
    "matched_terms": [
      "116.74",
      "E1R_REGIME_AWARE_V0_1",
      "E1R_REGIME_AWARE_V0_2",
      "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE",
      "e1r_composer",
      "e1r_sidecar",
      "e1r_sidecar_sleeve",
      "e1r_v0_2_backtest_summary",
      "market_entry_gate",
      "market_gate_enabled",
      "market_shock_daily_return",
      "market_shock_gate_enabled",
      "risk_off_below_spx_ma50",
      "run_stateful_simulation",
      "sidecar_active_by_regime"
    ],
    "sample_hits": [
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2A_ENGINE_ENTRYPOINT_REPORT.json",
        "line": 22,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "      \"name\": \"run_stateful_simulation\","
      },
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2A_ENGINE_ENTRYPOINT_REPORT.json",
        "line": 46,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "      \"body_head\": \"def run_stateful_simulation(\\n    symbols:        list[str],\\n    prices_map:     dict[str, list[float]],\\n    dates_map:      dict[str, list[str]],\\n    spx_prices:     list[float],\\n    spx_dates:      list[str],\\n    ohlc_map:       dict = None,\\n    assumptions:    dict = None,\\n    step:           int  = 1,\\n    min_history:    int  = 120,\\n    market_score_default: float = 60.0,\\n    sim_start_date: str  = None,  # 交易执行起始日（None=从 min_history 后开始）\\n    sim_end_date:   str  = None,  # 交易执行截止日（None=到末尾）\\n    ndx_prices:     list = None,  # NDX 收盘价（Gate v2 Leadership 判断）\\n    ndx_dates:      list = None,\\n    sox_prices:     list = None,  # SOX 收盘价\\n    sox_dates:      list = None,\\n    vix_prices:     list = None,  # VIX 收盘价\\n    vix_dates:      list = None,\\n) -> dict:\\n    \\\"\\\"\\\"\\n    Layer D v1.6: Strict Top3 + RS threshold + MinHold + Relative SPX Stop\\n\\n    修正项（相比 v3）：\\n    1. SPX master calendar — 时间轴以 SPX dates 为准\\n    2. Date-based alignment — 所有股票按日期查找，不用 index 直接对齐\\n    3. skipped_orders_by_reason — 跳过原因分类统计\\n    4. sample_validity 检查 — 样本不足时返回 INSUFFICIENT_SAMPLE\\n    \\\"\\\"\\\"\\n    logger.info(\\\"[Backtest Layer D v1.6] Strict Top3 + RS/MinHold/RelSt"
      },
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2A_ENGINE_ENTRYPOINT_REPORT.json",
        "line": 78,
        "matched": [
          "market_gate_enabled",
          "risk_off_below_spx_ma50",
          "market_shock_gate_enabled",
          "market_shock_daily_return"
        ],
        "text": "      \"body_head\": \"def run_strategy_variant_comparison(\\n    symbols: list[str],\\n    prices_map: dict[str, list[float]],\\n    dates_map: dict[str, list[str]],\\n    spx_prices: list[float],\\n    spx_dates: list[str],\\n    ndx_prices: list[float] = None,\\n    ndx_dates:  list[str]   = None,\\n    sox_prices: list[float] = None,\\n    sox_dates:  list[str]   = None,\\n    vix_prices: list[float] = None,\\n    vix_dates:  list[str]   = None,\\n) -> dict:\\n    \\\"\\\"\\\"\\n    Run four diagnostic portfolio variants using Strict Top3, no fixed TP.\\n\\n    V0_BASE: current Strict Top3 baseline.\\n    V1_RS95: raise entry RS threshold from 90 to 95.\\n    V2_RS95_MINHOLD5: add minimum 5 trading-day hold for ordinary REDUCE/EXIT.\\n    V3_RS95_MINHOLD5_RELSTOP8: add relative SPX underperformance stop.\\n\\n    Selection policy:\\n    1. Prefer PASS over PARTIAL over FAIL.\\n    2. Within the same status, prefer higher total return.\\n    3. Break ties with higher Profit Factor, higher Sharpe, then lower max drawdown.\\n    \\\"\\\"\\\"\\n    logger.info(\\\"[Backtest Layer D v1.6] Strategy Variant Comparison...\\\")\\n\\n    base = {\\n        **LAYER_D_ASSUMPTIONS,\\n        \\\"market_gate_enabled\\\": False,\\n        \\\"mark"
      },
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2A_ENGINE_ENTRYPOINT_REPORT.json",
        "line": 176,
        "matched": [
          "116.74"
        ],
        "text": "      \"body_head\": \"def build_spec() -> dict[str, Any]:\\n    return {\\n        \\\"strategy_id\\\": \\\"E1R_UNIFIED_5Y_FULL_ACCOUNT_V1\\\",\\n        \\\"purpose\\\": \\\"Run a single continuous 5Y full-account backtest that organically connects UPTREND, SIDEWAYS, and DOWNTREND regimes in one capital account.\\\",\\n        \\\"window\\\": {\\n            \\\"target_start\\\": \\\"2021-06-11\\\",\\n            \\\"target_end\\\": \\\"latest available aligned 5Y date before forward start\\\",\\n            \\\"expected_min_rows\\\": 1000,\\n        },\\n        \\\"capital_account\\\": {\\n            \\\"initial_capital\\\": 100000.0,\\n            \\\"single_account\\\": True,\\n            \\\"daily_mark_to_market\\\": True,\\n            \\\"fields_required_per_day\\\": [\\n                \\\"date\\\",\\n                \\\"cash\\\",\\n                \\\"market_value\\\",\\n                \\\"portfolio_value\\\",\\n                \\\"daily_return\\\",\\n                \\\"drawdown\\\",\\n                \\\"n_positions\\\",\\n                \\\"gross_exposure\\\",\\n                \\\"regime\\\",\\n                \\\"subclass\\\",\\n                \\\"actions\\\",\\n            ],\\n        },\\n        \\\"regime_rules_high_level\\\": {\\n            \\\"UPTREND\\\": \\\"Use E1R uptrend/core stateful posit"
      },
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2A_ENGINE_ENTRYPOINT_REPORT.json",
        "line": 185,
        "matched": [
          "e1r_composer"
        ],
        "text": "      \"body_head\": \"def load_existing_5y_generation_inputs() -> Dict[str, Any]:\\n    \\\"\\\"\\\"\\n    Dry-run only.\\n\\n    This function intentionally does not write canonical exports.\\n    It inspects whether the current repository has enough persisted inputs\\n    to generate E1R 5Y interval records:\\n      core_daily_equity_records + sidecar_records\\n      -> extract_core_interval_returns(...)\\n      -> build_equity_records_from_returns(...)\\n    \\\"\\\"\\\"\\n    from src.engine import e1r_composer as composer  # type: ignore\\n\\n    source_summary: Dict[str, Any] = {\\n        \\\"core_sources\\\": [],\\n        \\\"sidecar_sources\\\": [],\\n        \\\"interval_sources\\\": [],\\n    }\\n\\n    def list_shape(label: str, rows: Any) -> Dict[str, Any]:\\n        if not isinstance(rows, list):\\n            return {\\\"label\\\": label, \\\"is_list\\\": False}\\n        keys = set()\\n        for row in rows[:50]:\\n            if isinstance(row, dict):\\n                keys.update(row.keys())\\n        return {\\n            \\\"label\\\": label,\\n            \\\"is_list\\\": True,\\n            \\\"length\\\": len(rows),\\n            \\\"keys\\\": sorted(keys),\\n            \\\"has_core_minimum\\\": (\\n                \\\"date\\\" in keys and (\\"
      },
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2A_ENGINE_ENTRYPOINT_REPORT.json",
        "line": 212,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "      \"body_head\": \"def normalize_backtest_e1r_from_comparison(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:\\n    out = []\\n    for r in rows:\\n        d = get_date(r)\\n        e = as_float(r.get(\\\"e1r_direct_composed_equity\\\"))\\n        idx = as_float(r.get(\\\"e1r_direct_composed_indexed\\\"))\\n        if not d or e is None:\\n            continue\\n        out.append({\\n            \\\"date\\\": d,\\n            \\\"strategy_id\\\": \\\"E1R_REGIME_AWARE_V0_2_DIRECT_COMPOSED_CANDIDATE\\\",\\n            \\\"curve_type\\\": \\\"backtest_5y_candidate\\\",\\n            \\\"canonical\\\": False,\\n            \\\"warning\\\": \\\"NOT_FROZEN_E1R_V0_2\\\",\\n            \\\"equity\\\": e,\\n            \\\"indexed\\\": idx,\\n        })\\n    return out\""
      },
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2A_ENGINE_ENTRYPOINT_REPORT.json",
        "line": 224,
        "matched": [
          "e1r_sidecar",
          "e1r_sidecar_sleeve"
        ],
        "text": "      \"source\": \"src/engine/e1r_sidecar_sleeve.py\","
      },
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2A_ENGINE_ENTRYPOINT_REPORT.json",
        "line": 249,
        "matched": [
          "e1r_composer"
        ],
        "text": "      \"source\": \"src/engine/e1r_composer.py\","
      },
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2A_ENGINE_ENTRYPOINT_REPORT.json",
        "line": 261,
        "matched": [
          "e1r_composer"
        ],
        "text": "      \"source\": \"src/engine/e1r_composer.py\","
      },
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2A_ENGINE_ENTRYPOINT_REPORT.json",
        "line": 271,
        "matched": [
          "sidecar_active_by_regime"
        ],
        "text": "      \"body_head\": \"def summarize_combined_variant(\\n    interval_records: Sequence[dict[str, Any]],\\n    equity_records: Sequence[dict[str, Any]],\\n    initial_equity: float,\\n) -> dict[str, Any]:\\n    combined_returns = [safe_float(r.get(\\\"combined_return\\\")) or 0.0 for r in interval_records]\\n    core_returns = [safe_float(r.get(\\\"core_return\\\")) or 0.0 for r in interval_records]\\n    sidecar_returns = [safe_float(r.get(\\\"sidecar_return\\\")) or 0.0 for r in interval_records]\\n    spx_returns = [safe_float(r.get(\\\"spx_return\\\")) or 0.0 for r in interval_records]\\n\\n    equity_curve = [initial_equity] + [\\n        safe_float(r.get(\\\"equity\\\")) or initial_equity for r in equity_records\\n    ]\\n\\n    total_return = compound_return(combined_returns)\\n    core_return = compound_return(core_returns)\\n    sidecar_return = compound_return(sidecar_returns)\\n    spx_return = compound_return(spx_returns)\\n\\n    active_records = [r for r in interval_records if r.get(\\\"sidecar_active\\\")]\\n\\n    active_by_regime: dict[str, int] = {}\\n    active_by_subclass: dict[str, int] = {}\\n    contribution_by_regime: dict[str, float] = {}\\n    contribution_by_subclass: dict[str, float] = {}\\n\\n    for row "
      },
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2A_ENGINE_ENTRYPOINT_REPORT.json",
        "line": 274,
        "matched": [
          "e1r_composer"
        ],
        "text": "      \"source\": \"src/engine/e1r_composer.py\","
      },
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2A_ENGINE_ENTRYPOINT_REPORT.json",
        "line": 284,
        "matched": [
          "E1R_REGIME_AWARE_V0_2",
          "E1R_REGIME_AWARE_V0_1",
          "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE",
          "sidecar_active_by_regime"
        ],
        "text": "      \"body_head\": \"def compose_e1r_v0_2_variant(\\n    core_variant_result: dict[str, Any],\\n    sidecar_result: dict[str, Any],\\n    initial_equity: float = 100000.0,\\n) -> dict[str, Any]:\\n    core_records = core_variant_result.get(\\\"daily_equity_records\\\", [])\\n    sidecar_records = sidecar_result.get(\\\"records\\\", [])\\n\\n    interval_records = extract_core_interval_returns(core_records, sidecar_records)\\n    equity_records = build_equity_records_from_returns(interval_records, initial_equity)\\n    summary = summarize_combined_variant(interval_records, equity_records, initial_equity)\\n\\n    result = copy.deepcopy(core_variant_result)\\n\\n    sidecar_summary = sidecar_result.get(\\\"summary\\\", {}) or {}\\n\\n    result.update({\\n        \\\"strategy_id\\\": \\\"E1R_REGIME_AWARE_V0_2\\\",\\n        \\\"strategy_variant\\\": \\\"E1R_regime_aware_v0_2_formal_sidecar_sleeve\\\",\\n        \\\"version\\\": \\\"E1R-v0.2-formal-sidecar-sleeve\\\",\\n        \\\"research_status\\\": \\\"FORMAL_SIDECAR_SLEEVE_ENGINE\\\",\\n        \\\"core_total_trades\\\": core_variant_result.get(\\\"total_trades\\\"),\\n        \\\"sidecar_trade_count_approx\\\": sidecar_summary.get(\\\"trade_count_approx\\\"),\\n        \\\"combined_trade_count_note\\\": (\\n        "
      },
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2A_ENGINE_ENTRYPOINT_REPORT.json",
        "line": 309,
        "matched": [
          "e1r_v0_2_backtest_summary",
          "run_stateful_simulation"
        ],
        "text": "      \"body_head\": \"def infer_contract(defs_by_file: dict[str, Any], grep_by_file: dict[str, Any], import_probe: dict[str, Any]) -> dict[str, Any]:\\n    findings = []\\n    risks = []\\n    next_actions = []\\n\\n    generator_text = read_text(GENERATOR) if GENERATOR.exists() else \\\"\\\"\\n    composer_text = read_text(COMPOSER) if COMPOSER.exists() else \\\"\\\"\\n\\n    has_compose_call_in_generator = \\\"compose_e1r_v0_2_variant\\\" in generator_text\\n    has_core_var_in_generator = \\\"core_variant_result\\\" in generator_text\\n    has_sidecar_var_in_generator = \\\"sidecar_result\\\" in generator_text\\n    has_daily_in_generator = (\\\"daily_equity_records\\\" in generator_text) or (\\\"daily_records\\\" in generator_text) or (\\\"equity_curve\\\" in generator_text)\\n\\n    has_compose_def = \\\"def compose_e1r_v0_2_variant\\\" in composer_text\\n    compose_mentions_core = \\\"core_variant_result\\\" in composer_text\\n    compose_mentions_sidecar = \\\"sidecar_result\\\" in composer_text\\n    compose_mentions_daily = (\\\"daily_equity_records\\\" in composer_text) or (\\\"daily_records\\\" in composer_text) or (\\\"equity_curve\\\" in composer_text)\\n\\n    if has_compose_call_in_generator:\\n        findings.append(\\\"Generator references "
      },
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2A_ENGINE_ENTRYPOINT_REPORT.json",
        "line": 343,
        "matched": [
          "e1r_composer"
        ],
        "text": "      \"source\": \"scripts/instrument_e1r_composer_callsite_4b0j.py\","
      },
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2A_ENGINE_ENTRYPOINT_REPORT.json",
        "line": 421,
        "matched": [
          "e1r_sidecar",
          "e1r_sidecar_sleeve"
        ],
        "text": "      \"source\": \"src/engine/e1r_sidecar_sleeve.py\","
      },
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2A_ENGINE_ENTRYPOINT_REPORT.json",
        "line": 519,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "      \"body_head\": \"def normalize_e1r_oos(obj: Any) -> list[dict[str, Any]]:\\n    rows = extract_rows(obj)\\n    out = []\\n    first = None\\n    for r in rows:\\n        d = get_date(r)\\n        e = as_float(r.get(\\\"portfolio_value\\\") or r.get(\\\"equity\\\") or r.get(\\\"total_equity\\\"))\\n        if not d or e is None:\\n            continue\\n        if first is None:\\n            first = e\\n        out.append({\\n            \\\"date\\\": d,\\n            \\\"strategy_id\\\": r.get(\\\"strategy_id\\\") or \\\"E1R_REGIME_AWARE_V0_2\\\",\\n            \\\"curve_type\\\": \\\"forward_oos_kickoff_ready\\\",\\n            \\\"canonical\\\": False,\\n            \\\"warning\\\": \\\"E1R_FORWARD_KICKOFF_READY_NOT_OFFICIAL_LIVE\\\",\\n            \\\"equity\\\": e,\\n            \\\"indexed\\\": as_float(r.get(\\\"strategy_indexed\\\")) or (e / first * 100.0 if first else None),\\n            \\\"official_kickoff_date\\\": r.get(\\\"official_kickoff_date\\\"),\\n            \\\"market_state\\\": r.get(\\\"market_state\\\"),\\n            \\\"regime\\\": r.get(\\\"regime\\\"),\\n            \\\"subclass\\\": r.get(\\\"subclass\\\"),\\n            \\\"gross_exposure\\\": r.get(\\\"gross_exposure\\\"),\\n            \\\"core_exposure\\\": r.get(\\\"core_exposure\\\"),\\n            \\\"sidecar_exposure\\\": r.g"
      },
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2A_ENGINE_ENTRYPOINT_REPORT.json",
        "line": 538,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "    \"name\": \"run_stateful_simulation\","
      },
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2A_ENGINE_ENTRYPOINT_REPORT.json",
        "line": 562,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "    \"body_head\": \"def run_stateful_simulation(\\n    symbols:        list[str],\\n    prices_map:     dict[str, list[float]],\\n    dates_map:      dict[str, list[str]],\\n    spx_prices:     list[float],\\n    spx_dates:      list[str],\\n    ohlc_map:       dict = None,\\n    assumptions:    dict = None,\\n    step:           int  = 1,\\n    min_history:    int  = 120,\\n    market_score_default: float = 60.0,\\n    sim_start_date: str  = None,  # 交易执行起始日（None=从 min_history 后开始）\\n    sim_end_date:   str  = None,  # 交易执行截止日（None=到末尾）\\n    ndx_prices:     list = None,  # NDX 收盘价（Gate v2 Leadership 判断）\\n    ndx_dates:      list = None,\\n    sox_prices:     list = None,  # SOX 收盘价\\n    sox_dates:      list = None,\\n    vix_prices:     list = None,  # VIX 收盘价\\n    vix_dates:      list = None,\\n) -> dict:\\n    \\\"\\\"\\\"\\n    Layer D v1.6: Strict Top3 + RS threshold + MinHold + Relative SPX Stop\\n\\n    修正项（相比 v3）：\\n    1. SPX master calendar — 时间轴以 SPX dates 为准\\n    2. Date-based alignment — 所有股票按日期查找，不用 index 直接对齐\\n    3. skipped_orders_by_reason — 跳过原因分类统计\\n    4. sample_validity 检查 — 样本不足时返回 INSUFFICIENT_SAMPLE\\n    \\\"\\\"\\\"\\n    logger.info(\\\"[Backtest Layer D v1.6] Strict Top3 + RS/MinHold/RelStop"
      },
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2A_ENGINE_ENTRYPOINT_REPORT.json",
        "line": 570,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "          \"name\": \"run_stateful_simulation\","
      },
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2A_ENGINE_ENTRYPOINT_REPORT.json",
        "line": 595,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "          \"body_head\": \"def run_stateful_simulation(\\n    symbols:        list[str],\\n    prices_map:     dict[str, list[float]],\\n    dates_map:      dict[str, list[str]],\\n    spx_prices:     list[float],\\n    spx_dates:      list[str],\\n    ohlc_map:       dict = None,\\n    assumptions:    dict = None,\\n    step:           int  = 1,\\n    min_history:    int  = 120,\\n    market_score_default: float = 60.0,\\n    sim_start_date: str  = None,  # 交易执行起始日（None=从 min_history 后开始）\\n    sim_end_date:   str  = None,  # 交易执行截止日（None=到末尾）\\n    ndx_prices:     list = None,  # NDX 收盘价（Gate v2 Leadership 判断）\\n    ndx_dates:      list = None,\\n    sox_prices:     list = None,  # SOX 收盘价\\n    sox_dates:      list = None,\\n    vix_prices:     list = None,  # VIX 收盘价\\n    vix_dates:      list = None,\\n) -> dict:\\n    \\\"\\\"\\\"\\n    Layer D v1.6: Strict Top3 + RS threshold + MinHold + Relative SPX Stop\\n\\n    修正项（相比 v3）：\\n    1. SPX master calendar — 时间轴以 SPX dates 为准\\n    2. Date-based alignment — 所有股票按日期查找，不用 index 直接对齐\\n    3. skipped_orders_by_reason — 跳过原因分类统计\\n    4. sample_validity 检查 — 样本不足时返回 INSUFFICIENT_SAMPLE\\n    \\\"\\\"\\\"\\n    logger.info(\\\"[Backtest Layer D v1.6] Strict Top3 + RS/MinHold/R"
      },
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2A_ENGINE_ENTRYPOINT_REPORT.json",
        "line": 616,
        "matched": [
          "market_gate_enabled",
          "risk_off_below_spx_ma50",
          "market_shock_gate_enabled",
          "market_shock_daily_return"
        ],
        "text": "          \"body_head\": \"def run_strategy_variant_comparison(\\n    symbols: list[str],\\n    prices_map: dict[str, list[float]],\\n    dates_map: dict[str, list[str]],\\n    spx_prices: list[float],\\n    spx_dates: list[str],\\n    ndx_prices: list[float] = None,\\n    ndx_dates:  list[str]   = None,\\n    sox_prices: list[float] = None,\\n    sox_dates:  list[str]   = None,\\n    vix_prices: list[float] = None,\\n    vix_dates:  list[str]   = None,\\n) -> dict:\\n    \\\"\\\"\\\"\\n    Run four diagnostic portfolio variants using Strict Top3, no fixed TP.\\n\\n    V0_BASE: current Strict Top3 baseline.\\n    V1_RS95: raise entry RS threshold from 90 to 95.\\n    V2_RS95_MINHOLD5: add minimum 5 trading-day hold for ordinary REDUCE/EXIT.\\n    V3_RS95_MINHOLD5_RELSTOP8: add relative SPX underperformance stop.\\n\\n    Selection policy:\\n    1. Prefer PASS over PARTIAL over FAIL.\\n    2. Within the same status, prefer higher total return.\\n    3. Break ties with higher Profit Factor, higher Sharpe, then lower max drawdown.\\n    \\\"\\\"\\\"\\n    logger.info(\\\"[Backtest Layer D v1.6] Strategy Variant Comparison...\\\")\\n\\n    base = {\\n        **LAYER_D_ASSUMPTIONS,\\n        \\\"market_gate_enabled\\\": False,\\n        \\\""
      },
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2A_ENGINE_ENTRYPOINT_REPORT.json",
        "line": 839,
        "matched": [
          "e1r_sidecar",
          "e1r_sidecar_sleeve"
        ],
        "text": "          \"module\": \"src.engine.e1r_sidecar_sleeve\","
      },
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2A_ENGINE_ENTRYPOINT_REPORT.json",
        "line": 842,
        "matched": [
          "e1r_sidecar",
          "e1r_sidecar_sleeve"
        ],
        "text": "            \"build_e1r_sidecar_sleeve\""
      },
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2A_ENGINE_ENTRYPOINT_REPORT.json",
        "line": 847,
        "matched": [
          "e1r_composer"
        ],
        "text": "          \"module\": \"src.engine.e1r_composer\","
      },
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2A_ENGINE_ENTRYPOINT_REPORT.json",
        "line": 897,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "          \"call\": \"run_stateful_simulation\""
      },
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2A_ENGINE_ENTRYPOINT_REPORT.json",
        "line": 956,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "            \"run_stateful_simulation\""
      },
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2A_ENGINE_ENTRYPOINT_REPORT.json",
        "line": 977,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "              \"text\": \"def run_stateful_simulation(\""
      },
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2A_ENGINE_ENTRYPOINT_REPORT.json",
        "line": 3802,
        "matched": [
          "market_entry_gate"
        ],
        "text": "              \"text\": \"        \\\"market_entry_gate\\\": {\""
      },
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2A_ENGINE_ENTRYPOINT_REPORT.json",
        "line": 3810,
        "matched": [
          "market_gate_enabled"
        ],
        "text": "              \"text\": \"            \\\"enabled\\\": market_gate_enabled,\""
      },
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2A_ENGINE_ENTRYPOINT_REPORT.json",
        "line": 4081,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "            \"run_stateful_simulation\""
      }
    ]
  },
  {
    "path": "docs/research/E1R_V0_2_STAGE3_8E2F1A_FORWARD_SOURCE_AUDIT.json",
    "score": 5140,
    "hit_count": 106,
    "matched_terms": [
      "E1R_REGIME_AWARE_V0_1",
      "E1R_REGIME_AWARE_V0_2",
      "e1r_composer",
      "e1r_sidecar",
      "e1r_sidecar_sleeve",
      "e1r_v0_2_backtest_summary",
      "market_entry_gate",
      "market_gate_enabled",
      "market_shock_daily_return",
      "market_shock_gate_enabled",
      "run_stateful_simulation",
      "sidecar_active_by_regime"
    ],
    "sample_hits": [
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F1A_FORWARD_SOURCE_AUDIT.json",
        "line": 28,
        "matched": [
          "e1r_composer"
        ],
        "text": "    \"src/engine/e1r_composer.py\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F1A_FORWARD_SOURCE_AUDIT.json",
        "line": 29,
        "matched": [
          "e1r_sidecar",
          "e1r_sidecar_sleeve"
        ],
        "text": "    \"src/engine/e1r_sidecar_sleeve.py\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F1A_FORWARD_SOURCE_AUDIT.json",
        "line": 680,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "        \"E1R_REGIME_AWARE_V0_2\": ["
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F1A_FORWARD_SOURCE_AUDIT.json",
        "line": 830,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "          \"term\": \"E1R_REGIME_AWARE_V0_2\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F1A_FORWARD_SOURCE_AUDIT.json",
        "line": 832,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "          \"text\": \"    strategy_id = status.get(\\\"strategy_id\\\", \\\"E1R_REGIME_AWARE_V0_2\\\")\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F1A_FORWARD_SOURCE_AUDIT.json",
        "line": 1522,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "        \"E1R_REGIME_AWARE_V0_2\": ["
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F1A_FORWARD_SOURCE_AUDIT.json",
        "line": 1755,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "          \"term\": \"E1R_REGIME_AWARE_V0_2\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F1A_FORWARD_SOURCE_AUDIT.json",
        "line": 1757,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "          \"text\": \"        \\\"strategy_id\\\": \\\"E1R_REGIME_AWARE_V0_2\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F1A_FORWARD_SOURCE_AUDIT.json",
        "line": 2776,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "        \"E1R_REGIME_AWARE_V0_2\": ["
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F1A_FORWARD_SOURCE_AUDIT.json",
        "line": 2868,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "          \"term\": \"E1R_REGIME_AWARE_V0_2\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F1A_FORWARD_SOURCE_AUDIT.json",
        "line": 2870,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "          \"text\": \"        \\\"strategy_id\\\": \\\"E1R_REGIME_AWARE_V0_2\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F1A_FORWARD_SOURCE_AUDIT.json",
        "line": 3085,
        "matched": [
          "e1r_sidecar",
          "e1r_sidecar_sleeve"
        ],
        "text": "          \"text\": \"from src.engine.e1r_sidecar_sleeve import E1RSidecarConfig, build_e1r_sidecar_sleeve\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F1A_FORWARD_SOURCE_AUDIT.json",
        "line": 3090,
        "matched": [
          "e1r_sidecar",
          "e1r_sidecar_sleeve"
        ],
        "text": "          \"text\": \"    sidecar_result = build_e1r_sidecar_sleeve(\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F1A_FORWARD_SOURCE_AUDIT.json",
        "line": 3243,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "        \"E1R_REGIME_AWARE_V0_2\": ["
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F1A_FORWARD_SOURCE_AUDIT.json",
        "line": 3355,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "          \"term\": \"E1R_REGIME_AWARE_V0_2\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F1A_FORWARD_SOURCE_AUDIT.json",
        "line": 3357,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "          \"text\": \"    v2 = extract_variant(variants, \\\"E1R_REGIME_AWARE_V0_2\\\")\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F1A_FORWARD_SOURCE_AUDIT.json",
        "line": 3360,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "          \"term\": \"E1R_REGIME_AWARE_V0_2\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F1A_FORWARD_SOURCE_AUDIT.json",
        "line": 3362,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "          \"text\": \"        \\\"strategy_id\\\": \\\"E1R_REGIME_AWARE_V0_2\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F1A_FORWARD_SOURCE_AUDIT.json",
        "line": 3365,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "          \"term\": \"E1R_REGIME_AWARE_V0_2\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F1A_FORWARD_SOURCE_AUDIT.json",
        "line": 3367,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "          \"text\": \"            \\\"strategy_id\\\": \\\"E1R_REGIME_AWARE_V0_2\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F1A_FORWARD_SOURCE_AUDIT.json",
        "line": 3370,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "          \"term\": \"E1R_REGIME_AWARE_V0_2\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F1A_FORWARD_SOURCE_AUDIT.json",
        "line": 3372,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "          \"text\": \"            \\\"E1R_REGIME_AWARE_V0_2\\\": v2_curve,\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F1A_FORWARD_SOURCE_AUDIT.json",
        "line": 3422,
        "matched": [
          "e1r_v0_2_backtest_summary"
        ],
        "text": "          \"text\": \"    write_json(ROOT / \\\"exports/e1r_v0_2_backtest_summary.json\\\", summary)\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F1A_FORWARD_SOURCE_AUDIT.json",
        "line": 3432,
        "matched": [
          "e1r_v0_2_backtest_summary"
        ],
        "text": "          \"text\": \"    print(\\\"Wrote exports/e1r_v0_2_backtest_summary.json\\\")\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F1A_FORWARD_SOURCE_AUDIT.json",
        "line": 3702,
        "matched": [
          "sidecar_active_by_regime"
        ],
        "text": "          \"text\": \"            \\\"sidecar_active_by_regime\\\": v2.get(\\\"sidecar_active_by_regime\\\"),\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F1A_FORWARD_SOURCE_AUDIT.json",
        "line": 3722,
        "matched": [
          "sidecar_active_by_regime"
        ],
        "text": "          \"text\": \"            \\\"sidecar_active_by_regime\\\": v2.get(\\\"sidecar_active_by_regime\\\"),\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F1A_FORWARD_SOURCE_AUDIT.json",
        "line": 3820,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "        \"E1R_REGIME_AWARE_V0_2\": ["
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F1A_FORWARD_SOURCE_AUDIT.json",
        "line": 3924,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "          \"term\": \"E1R_REGIME_AWARE_V0_2\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F1A_FORWARD_SOURCE_AUDIT.json",
        "line": 3926,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "          \"text\": \"        \\\"strategy_id\\\": \\\"E1R_REGIME_AWARE_V0_2\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F1A_FORWARD_SOURCE_AUDIT.json",
        "line": 3929,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "          \"term\": \"E1R_REGIME_AWARE_V0_2\","
      }
    ]
  }
]
```

## Candidate Scripts
```json
[
  {
    "path": "scripts/e1r_k2_r9b_115_return_artifact_recovery.py",
    "score": 3460,
    "hit_count": 39,
    "matched_terms": [
      "116.74",
      "116.7435999134756",
      "D3_RISK_OFF_PLUS_SHOCK_GATE",
      "E1R_REGIME_AWARE_V0_1",
      "E1R_REGIME_AWARE_V0_2",
      "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE",
      "e1r_composer",
      "e1r_sidecar",
      "e1r_sidecar_sleeve",
      "e1r_v0_2_backtest_summary",
      "market_entry_gate",
      "market_gate_enabled",
      "market_shock_daily_return",
      "market_shock_gate_enabled",
      "risk_off_below_spx_ma50",
      "run_stateful_simulation",
      "sidecar_active_by_regime"
    ],
    "sample_hits": [
      {
        "path": "scripts/e1r_k2_r9b_115_return_artifact_recovery.py",
        "line": 14,
        "matched": [
          "e1r_v0_2_backtest_summary"
        ],
        "text": "TARGET_ARTIFACT = ROOT / \"exports/e1r_v0_2_backtest_summary.json\""
      },
      {
        "path": "scripts/e1r_k2_r9b_115_return_artifact_recovery.py",
        "line": 26,
        "matched": [
          "e1r_sidecar",
          "e1r_sidecar_sleeve"
        ],
        "text": "    ROOT / \"src/engine/e1r_sidecar_sleeve.py\","
      },
      {
        "path": "scripts/e1r_k2_r9b_115_return_artifact_recovery.py",
        "line": 27,
        "matched": [
          "e1r_composer"
        ],
        "text": "    ROOT / \"src/engine/e1r_composer.py\","
      },
      {
        "path": "scripts/e1r_k2_r9b_115_return_artifact_recovery.py",
        "line": 45,
        "matched": [
          "116.7435999134756",
          "116.74"
        ],
        "text": "TARGET_RETURN = 116.7435999134756"
      },
      {
        "path": "scripts/e1r_k2_r9b_115_return_artifact_recovery.py",
        "line": 48,
        "matched": [
          "e1r_v0_2_backtest_summary"
        ],
        "text": "    \"e1r_v0_2_backtest_summary\","
      },
      {
        "path": "scripts/e1r_k2_r9b_115_return_artifact_recovery.py",
        "line": 49,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "    \"E1R_REGIME_AWARE_V0_2\","
      },
      {
        "path": "scripts/e1r_k2_r9b_115_return_artifact_recovery.py",
        "line": 50,
        "matched": [
          "E1R_REGIME_AWARE_V0_1"
        ],
        "text": "    \"E1R_REGIME_AWARE_V0_1\","
      },
      {
        "path": "scripts/e1r_k2_r9b_115_return_artifact_recovery.py",
        "line": 51,
        "matched": [
          "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE"
        ],
        "text": "    \"UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE\","
      },
      {
        "path": "scripts/e1r_k2_r9b_115_return_artifact_recovery.py",
        "line": 52,
        "matched": [
          "sidecar_active_by_regime"
        ],
        "text": "    \"sidecar_active_by_regime\","
      },
      {
        "path": "scripts/e1r_k2_r9b_115_return_artifact_recovery.py",
        "line": 53,
        "matched": [
          "D3_RISK_OFF_PLUS_SHOCK_GATE"
        ],
        "text": "    \"D3_RISK_OFF_PLUS_SHOCK_GATE\","
      },
      {
        "path": "scripts/e1r_k2_r9b_115_return_artifact_recovery.py",
        "line": 54,
        "matched": [
          "market_entry_gate"
        ],
        "text": "    \"market_entry_gate\","
      },
      {
        "path": "scripts/e1r_k2_r9b_115_return_artifact_recovery.py",
        "line": 55,
        "matched": [
          "market_gate_enabled"
        ],
        "text": "    \"market_gate_enabled\","
      },
      {
        "path": "scripts/e1r_k2_r9b_115_return_artifact_recovery.py",
        "line": 56,
        "matched": [
          "risk_off_below_spx_ma50"
        ],
        "text": "    \"risk_off_below_spx_ma50\","
      },
      {
        "path": "scripts/e1r_k2_r9b_115_return_artifact_recovery.py",
        "line": 57,
        "matched": [
          "market_shock_gate_enabled"
        ],
        "text": "    \"market_shock_gate_enabled\","
      },
      {
        "path": "scripts/e1r_k2_r9b_115_return_artifact_recovery.py",
        "line": 58,
        "matched": [
          "market_shock_daily_return"
        ],
        "text": "    \"market_shock_daily_return\","
      }
    ],
    "ast_summary": {
      "path": "scripts/e1r_k2_r9b_115_return_artifact_recovery.py",
      "parse_ok": true,
      "imports": [
        {
          "line": 2,
          "text": "from __future__ import annotations"
        },
        {
          "line": 4,
          "text": "from pathlib import Path"
        },
        {
          "line": 5,
          "text": "import ast"
        },
        {
          "line": 6,
          "text": "import json"
        },
        {
          "line": 7,
          "text": "import hashlib"
        },
        {
          "line": 8,
          "text": "import re"
        },
        {
          "line": 9,
          "text": "from datetime import datetime, timezone"
        },
        {
          "line": 10,
          "text": "from typing import Any"
        }
      ],
      "functions": [
        {
          "name": "now",
          "line": 68,
          "end_line": 69
        },
        {
          "name": "rel",
          "line": 72,
          "end_line": 76
        },
        {
          "name": "sha256",
          "line": 79,
          "end_line": 84
        },
        {
          "name": "read_json",
          "line": 87,
          "end_line": 88
        },
        {
          "name": "write_json",
          "line": 91,
          "end_line": 93
        },
        {
          "name": "safe_read_text",
          "line": 96,
          "end_line": 103
        },
        {
          "name": "is_excluded",
          "line": 106,
          "end_line": 107
        },
        {
          "name": "iter_files",
          "line": 110,
          "end_line": 121
        },
        {
          "name": "grep_needles",
          "line": 124,
          "end_line": 141
        },
        {
          "name": "score_hit",
          "line": 144,
          "end_line": 171
        },
        {
          "name": "group_hits",
          "line": 174,
          "end_line": 192
        },
        {
          "name": "parse_py_file",
          "line": 195,
          "end_line": 264
        },
        {
          "name": "analyze_candidate_scripts",
          "line": 267,
          "end_line": 282
        },
        {
          "name": "compact",
          "line": 285,
          "end_line": 299
        },
        {
          "name": "flatten_json",
          "line": 302,
          "end_line": 314
        },
        {
          "name": "inspect_target_artifact",
          "line": 317,
          "end_line": 342
        },
        {
          "name": "inspect_known_source_files",
          "line": 345,
          "end_line": 373
        },
        {
          "name": "derive_evidence_status",
          "line": 376,
          "end_line": 436
        },
        {
          "name": "main",
          "line": 439,
          "end_line": 657
        }
      ],
      "calls": [
        {
          "line": 93,
          "call": "path.write_text",
          "text": "path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + \"\\n\")"
        },
        {
          "line": 639,
          "call": "REPORT_MD.write_text",
          "text": "REPORT_MD.write_text(\"\\n\".join(md))"
        },
        {
          "line": 640,
          "call": "ARCH_MD.write_text",
          "text": "ARCH_MD.write_text(\"\\n\".join(md))"
        },
        {
          "line": 291,
          "call": "json.dumps",
          "text": "json.dumps(v, ensure_ascii=False)"
        },
        {
          "line": 600,
          "call": "json.dumps",
          "text": "json.dumps(target, indent=2, ensure_ascii=False)"
        },
        {
          "line": 605,
          "call": "json.dumps",
          "text": "json.dumps(evidence_status, indent=2, ensure_ascii=False)"
        },
        {
          "line": 610,
          "call": "json.dumps",
          "text": "json.dumps(grouped[\"by_path\"][:20], indent=2, ensure_ascii=False)"
        },
        {
          "line": 615,
          "call": "json.dumps",
          "text": "json.dumps(candidate_scripts[:20], indent=2, ensure_ascii=False)"
        },
        {
          "line": 620,
          "call": "json.dumps",
          "text": "json.dumps(known_source_files, indent=2, ensure_ascii=False)"
        },
        {
          "line": 625,
          "call": "json.dumps",
          "text": "json.dumps(unresolved, indent=2, ensure_ascii=False)"
        },
        {
          "line": 630,
          "call": "json.dumps",
          "text": "json.dumps(validations, indent=2, ensure_ascii=False)"
        },
        {
          "line": 635,
          "call": "json.dumps",
          "text": "json.dumps(decision, indent=2, ensure_ascii=False)"
        },
        {
          "line": 644,
          "call": "json.dumps",
          "text": "json.dumps(target, ensure_ascii=False)"
        },
        {
          "line": 645,
          "call": "json.dumps",
          "text": "json.dumps(evidence_status, ensure_ascii=False)"
        },
        {
          "line": 646,
          "call": "json.dumps",
          "text": "json.dumps(grouped[\"by_path\"][:10], ensure_ascii=False)"
        },
        {
          "line": 647,
          "call": "json.dumps",
          "text": "json.dumps(candidate_scripts[:10], ensure_ascii=False)"
        },
        {
          "line": 648,
          "call": "json.dumps",
          "text": "json.dumps(unresolved, ensure_ascii=False)"
        },
        {
          "line": 649,
          "call": "json.dumps",
          "text": "json.dumps(validations, ensure_ascii=False)"
        },
        {
          "line": 650,
          "call": "json.dumps",
          "text": "json.dumps(decision, ensure_ascii=False)"
        },
        {
          "line": 93,
          "call": "json.dumps",
          "text": "json.dumps(obj, indent=2, ensure_ascii=False)"
        }
      ],
      "assignments": [
        {
          "line": 14,
          "text": "TARGET_ARTIFACT = ROOT / \"exports/e1r_v0_2_backtest_summary.json\""
        },
        {
          "line": 24,
          "text": "FROZEN_STRATEGY_FILES = [\n    ROOT / \"src/engine/backtest.py\",\n    ROOT / \"src/engine/e1r_sidecar_sleeve.py\",\n    ROOT / \"src/engine/e1r_composer.py\",\n]"
        },
        {
          "line": 45,
          "text": "TARGET_RETURN = 116.7435999134756"
        },
        {
          "line": 47,
          "text": "NEEDLES = [\n    \"e1r_v0_2_backtest_summary\",\n    \"E1R_REGIME_AWARE_V0_2\",\n    \"E1R_REGIME_AWARE_V0_1\",\n    \"UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE\",\n    \"sidecar_active_by_regime\",\n    \"D3_RISK_OFF_PLUS_SHOCK_GATE\",\n    \"market_entry_gate\",\n    \"market_gate_enabled\",\n    \"risk_off_below_spx_ma50\",\n    \"market_shock_gate_enabled\",\n    \"market_shock_daily_return\",\n    \"run_stateful_simulation\",\n    \"e1r_sidecar\",\n    \"e1r_sidecar_sleeve\",\n    \"e1r_composer\",\n    \"116.7435999134756\",\n    \"116.74\",\n]"
        },
        {
          "line": 346,
          "text": "known = [\n        ROOT / \"src/engine/backtest.py\",\n        ROOT / \"src/engine/e1r_composer.py\",\n        ROOT / \"src/engine/e1r_sidecar_sleeve.py\",\n        ROOT / \"run_backtest.py\",\n    ]"
        },
        {
          "line": 379,
          "text": "generator_candidates = [\n        c for c in candidate_scripts\n        if any(\"e1r_v0_2_backtest_summary\" in t for t in c.get(\"matched_terms\", []))\n    ]"
        },
        {
          "line": 520,
          "text": "decision = {\n        \"k2_r9b_115_return_artifact_recovery_passed\": all([\n            validations[\"strategy_files_unchanged\"],\n            validations[\"target_artifact_exists\"],\n            validations[\"target_return_verified\"],\n            validations[\"repository_grep_completed\"],\n            validations[\"candidate_script_analysis_completed\"],\n            validations[\"known_source_files_inspected\"],\n        ]),\n        \"market_state_115_replication_ready\": blocking_count == 0,\n        \"formula_patch_allowed_now\": False,\n        \"candidate_extraction_allowed_now\": False,\n        \"implementation_may_resume\": False,\n        \"unresolved\": unresolved,\n        \"next_required_stage_if_ready\": \"4C-2C-4E-ENGINE-K2-R10-MARKET_GATE_STANDALONE_REPLICATION_PROPOSAL\",\n        \"next_required_stage_if_not_ready\": \"4C-2C-4E-ENGINE-K2-R9C-115_RETURN_GENERATOR_TRACE\",\n        \"conclusion\": (\n            \"K2_R9B_PASS_ARTIFACT_RECOVERY_READY_FOR_REPLICATION_PROPOSAL\"\n            if blocking_count == 0\n            else \"K2_R9B_RECOVERY_COMPLETE_NEEDS_GENERATOR_TRACE_OR_PARAM_EVIDENCE\"\n        ),\n        \"recommended_next_action\": (\n            \"If blocking unresolved remains, trace the generator script/call chain more narrowly and inspect the source lines \"\n            \"that produced E1R_REGIME_AWARE_V0_2 and regime_aware_logic. Do not patch.\"\n        ),\n    }"
        },
        {
          "line": 547,
          "text": "report = {\n        \"generated_at\": now(),\n        \"elapsed_seconds\": (datetime.now(timezone.utc) - started).total_seconds(),\n        \"stage\": \"4C-2C-4E-ENGINE-K2-R9B-115_RETURN_ARTIFACT_RECOVERY\",\n        \"status\": \"115_RETURN_ARTIFACT_RECOVERY_COMPLETE\",\n        \"purpose\": \"Recover the generation chain and parameter evidence for exports/e1r_v0_2_backtest_summary.json without changing strategy logic.\",\n        \"policy\": {\n            \"strategy_logic_changed\": False,\n            \"audit_only\": True,\n            \"formula_not_patched\": True,\n            \"backtest_engine_run\": False,\n            \"short_window_existing_engine_run\": False,\n            \"full_5y_backtest_run\": False,\n            \"forward_runner_run\": False,\n            \"candidate_generation_extracted\": False,\n            \"buy_add_reduce_exit_extracted\": False,\n            \"official_result_generated\": False,\n            \"dashboard_changed\": False,\n            \"frozen_strategy_files_changed\": before_hashes != after_hashes,\n        },\n        \"source\": {\n            \"k2_r9\": rel(K2_R9),\n            \"k2_r8\": rel(K2_R8),\n            \"target_artifact\": rel(TARGET_ARTIFACT),\n            \"search_dirs\": [rel(x) for x in SEARCH_DIRS],\n        },\n        \"target_artifact_inspection\": target,\n        \"evidence_status\": evidence_status,\n        \"grep_summary\": {\n            \"total_hits\": len(hits),\n            \"top_paths\": grouped[\"by_path\"][:20],\n        },\n        \"candidate_scripts\": candidate_scripts[:20],\n        \"known_sourc"
        },
        {
          "line": 463,
          "text": "prior_unresolved_filtered = [\n            x for x in prior_unresolved\n            if x.get(\"field\") not in {\n                \"market_entry_gate\",\n                \"market_gate_enabled\",\n                \"risk_off_below_spx_ma50\",\n                \"market_shock_gate_enabled\",\n                \"market_shock_daily_return\",\n            }\n        ]"
        }
      ]
    }
  }
]
```

## Known Source Files
```json
{
  "src/engine/backtest.py": {
    "exists": true,
    "sha256": "906605eacae917f8288a3cf5d76bea5596b01f774d810ae24c3df9ef46230aea",
    "hits": [
      {
        "line": 59,
        "matched": [
          "market_gate_enabled"
        ],
        "text": "    \"market_gate_enabled\": False,"
      },
      {
        "line": 60,
        "matched": [
          "risk_off_below_spx_ma50"
        ],
        "text": "    \"risk_off_below_spx_ma50\": False,"
      },
      {
        "line": 61,
        "matched": [
          "market_shock_gate_enabled"
        ],
        "text": "    \"market_shock_gate_enabled\": False,"
      },
      {
        "line": 62,
        "matched": [
          "market_shock_daily_return"
        ],
        "text": "    \"market_shock_daily_return\": -0.02,"
      },
      {
        "line": 763,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "def run_stateful_simulation("
      },
      {
        "line": 847,
        "matched": [
          "market_gate_enabled"
        ],
        "text": "    market_gate_enabled = bool(a.get(\"market_gate_enabled\", True))"
      },
      {
        "line": 848,
        "matched": [
          "risk_off_below_spx_ma50"
        ],
        "text": "    risk_off_below_spx_ma50 = bool(a.get(\"risk_off_below_spx_ma50\", True))"
      },
      {
        "line": 896,
        "matched": [
          "market_shock_gate_enabled"
        ],
        "text": "    market_shock_gate_enabled = bool(a.get(\"market_shock_gate_enabled\", True))"
      },
      {
        "line": 897,
        "matched": [
          "market_shock_daily_return"
        ],
        "text": "    market_shock_daily_return = float(a.get(\"market_shock_daily_return\", -0.02))"
      },
      {
        "line": 912,
        "matched": [
          "market_gate_enabled"
        ],
        "text": "        \"D1_NO_MARKET_GATE\" if not market_gate_enabled else"
      },
      {
        "line": 913,
        "matched": [
          "market_shock_gate_enabled"
        ],
        "text": "        \"D2_RISK_OFF_GATE\" if not market_shock_gate_enabled else"
      },
      {
        "line": 914,
        "matched": [
          "D3_RISK_OFF_PLUS_SHOCK_GATE"
        ],
        "text": "        \"D3_RISK_OFF_PLUS_SHOCK_GATE\""
      },
      {
        "line": 928,
        "matched": [
          "market_gate_enabled"
        ],
        "text": "    logger.info(f\"  Market Gate: enabled={market_gate_enabled} \""
      },
      {
        "line": 929,
        "matched": [
          "risk_off_below_spx_ma50"
        ],
        "text": "                f\"| RiskOff=SPX<MA50:{risk_off_below_spx_ma50} \""
      },
      {
        "line": 930,
        "matched": [
          "market_shock_gate_enabled",
          "market_shock_daily_return"
        ],
        "text": "                f\"| Shock<={market_shock_daily_return*100:.1f}%:{market_shock_gate_enabled}\")"
      },
      {
        "line": 938,
        "matched": [
          "market_gate_enabled"
        ],
        "text": "                f\"relstop={relative_stop_enabled} gate={market_gate_enabled} ──\")"
      },
      {
        "line": 1393,
        "matched": [
          "market_gate_enabled"
        ],
        "text": "        if not market_gate_enabled:"
      },
      {
        "line": 1449,
        "matched": [
          "market_shock_gate_enabled"
        ],
        "text": "                market_shock_gate_enabled"
      },
      {
        "line": 1450,
        "matched": [
          "market_shock_daily_return"
        ],
        "text": "                and spx_day_return <= market_shock_daily_return"
      },
      {
        "line": 1820,
        "matched": [
          "market_gate_enabled"
        ],
        "text": "                    if market_gate_enabled and len(holdings) >= entry_capacity:"
      },
      {
        "line": 1872,
        "matched": [
          "market_gate_enabled"
        ],
        "text": "                    if market_gate_enabled and len(holdings) >= entry_capacity:"
      },
      {
        "line": 1997,
        "matched": [
          "market_gate_enabled"
        ],
        "text": "                if action == \"ADD\" and market_gate_enabled and market_state in (\"CAUTIOUS_ON\", \"CASH_MODE\"):"
      },
      {
        "line": 2404,
        "matched": [
          "market_entry_gate"
        ],
        "text": "        \"market_entry_gate\": {"
      },
      {
        "line": 2406,
        "matched": [
          "market_gate_enabled"
        ],
        "text": "            \"enabled\": market_gate_enabled,"
      },
      {
        "line": 2407,
        "matched": [
          "risk_off_below_spx_ma50"
        ],
        "text": "            \"risk_off_rule\": \"SPX close < SPX MA50\" if risk_off_below_spx_ma50 else \"disabled\","
      },
      {
        "line": 2409,
        "matched": [
          "market_shock_daily_return"
        ],
        "text": "                f\"SPX daily return <= {market_shock_daily_return*100:.1f}%\""
      },
      {
        "line": 2410,
        "matched": [
          "market_shock_gate_enabled"
        ],
        "text": "                if market_shock_gate_enabled else \"disabled\""
      },
      {
        "line": 2519,
        "matched": [
          "market_gate_enabled"
        ],
        "text": "        \"market_gate_enabled\": False,"
      },
      {
        "line": 2520,
        "matched": [
          "market_shock_gate_enabled"
        ],
        "text": "        \"market_shock_gate_enabled\": False,"
      },
      {
        "line": 2526,
        "matched": [
          "market_gate_enabled"
        ],
        "text": "        \"market_gate_enabled\":       True,"
      },
      {
        "line": 2527,
        "matched": [
          "risk_off_below_spx_ma50"
        ],
        "text": "        \"risk_off_below_spx_ma50\":   True,"
      },
      {
        "line": 2528,
        "matched": [
          "market_shock_gate_enabled"
        ],
        "text": "        \"market_shock_gate_enabled\": True,"
      },
      {
        "line": 2529,
        "matched": [
          "market_shock_daily_return"
        ],
        "text": "        \"market_shock_daily_return\": -0.02,"
      },
      {
        "line": 2537,
        "matched": [
          "market_gate_enabled"
        ],
        "text": "        \"market_gate_enabled\":       True,"
      },
      {
        "line": 2538,
        "matched": [
          "risk_off_below_spx_ma50"
        ],
        "text": "        \"risk_off_below_spx_ma50\":   False,"
      },
      {
        "line": 2539,
        "matched": [
          "market_shock_gate_enabled"
        ],
        "text": "        \"market_shock_gate_enabled\": False,"
      },
      {
        "line": 2540,
        "matched": [
          "market_shock_daily_return"
        ],
        "text": "        \"market_shock_daily_return\": -0.02,"
      },
      {
        "line": 2579,
        "matched": [
          "E1R_REGIME_AWARE_V0_1"
        ],
        "text": "        \"E1R_REGIME_AWARE_V0_1\": {"
      },
      {
        "line": 2581,
        "matched": [
          "E1R_REGIME_AWARE_V0_1"
        ],
        "text": "            \"strategy_variant\":      \"E1R_regime_aware_v0_1_shell\","
      },
      {
        "line": 2646,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "            _result = run_stateful_simulation("
      },
      {
        "line": 2695,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "    # - Do not modify run_stateful_simulation()."
      },
      {
        "line": 2696,
        "matched": [
          "E1R_REGIME_AWARE_V0_1"
        ],
        "text": "    # - Do not modify E1R_REGIME_AWARE_V0_1."
      },
      {
        "line": 2704,
        "matched": [
          "e1r_sidecar",
          "e1r_sidecar_sleeve"
        ],
        "text": "        from src.engine.e1r_sidecar_sleeve import ("
      },
      {
        "line": 2706,
        "matched": [
          "e1r_sidecar",
          "e1r_sidecar_sleeve"
        ],
        "text": "            build_e1r_sidecar_sleeve,"
      },
      {
        "line": 2708,
        "matched": [
          "e1r_composer"
        ],
        "text": "        from src.engine.e1r_composer import compose_e1r_v0_2_variant"
      },
      {
        "line": 2710,
        "matched": [
          "E1R_REGIME_AWARE_V0_1"
        ],
        "text": "        _core_e1r = variant_results.get(\"E1R_REGIME_AWARE_V0_1\")"
      },
      {
        "line": 2730,
        "matched": [
          "e1r_sidecar",
          "e1r_sidecar_sleeve"
        ],
        "text": "            _sidecar_result = build_e1r_sidecar_sleeve("
      },
      {
        "line": 2737,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "            variant_results[\"E1R_REGIME_AWARE_V0_2\"] = compose_e1r_v0_2_variant("
      }
    ],
    "hit_count": 48
  },
  "src/engine/e1r_composer.py": {
    "exists": true,
    "sha256": "d65f48f7d34b0e3bb30544fcd36b2abf64435469c3a1bb695e9df05587eaf63f",
    "hits": [
      {
        "line": 5,
        "matched": [
          "E1R_REGIME_AWARE_V0_1"
        ],
        "text": "- E1R_REGIME_AWARE_V0_1 core daily equity records"
      },
      {
        "line": 9,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "- E1R_REGIME_AWARE_V0_2 formal combined daily equity records"
      },
      {
        "line": 270,
        "matched": [
          "sidecar_active_by_regime"
        ],
        "text": "        \"sidecar_active_by_regime\": active_by_regime,"
      },
      {
        "line": 300,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2\","
      },
      {
        "line": 301,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "        \"strategy_variant\": \"E1R_regime_aware_v0_2_formal_sidecar_sleeve\","
      },
      {
        "line": 312,
        "matched": [
          "E1R_REGIME_AWARE_V0_1"
        ],
        "text": "            \"core_variant\": \"E1R_REGIME_AWARE_V0_1\","
      },
      {
        "line": 344,
        "matched": [
          "sidecar_active_by_regime"
        ],
        "text": "    result[\"sidecar_active_by_regime\"] = summary[\"sidecar_active_by_regime\"]"
      },
      {
        "line": 351,
        "matched": [
          "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE"
        ],
        "text": "        \"regime_aware_logic\": \"UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE\","
      },
      {
        "line": 353,
        "matched": [
          "E1R_REGIME_AWARE_V0_1"
        ],
        "text": "        \"e1r_v0_2_core_variant\": \"E1R_REGIME_AWARE_V0_1\","
      }
    ],
    "hit_count": 9
  },
  "src/engine/e1r_sidecar_sleeve.py": {
    "exists": true,
    "sha256": "f5465d6d406cf6cf2d76ced8949fea04ebae825a119de51149104ce952fd6995",
    "hits": [
      {
        "line": 6,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "Formal engine module for E1R_REGIME_AWARE_V0_2 sidecar sleeve."
      },
      {
        "line": 19,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "This is intentionally separate from run_stateful_simulation()."
      },
      {
        "line": 23,
        "matched": [
          "E1R_REGIME_AWARE_V0_1"
        ],
        "text": "- E1R_REGIME_AWARE_V0_1 core"
      },
      {
        "line": 27,
        "matched": [
          "e1r_composer"
        ],
        "text": "e1r_composer.py."
      },
      {
        "line": 538,
        "matched": [
          "e1r_sidecar",
          "e1r_sidecar_sleeve"
        ],
        "text": "def build_e1r_sidecar_sleeve("
      },
      {
        "line": 564,
        "matched": [
          "e1r_sidecar",
          "e1r_sidecar_sleeve"
        ],
        "text": "        \"engine\": \"e1r_sidecar_sleeve\","
      }
    ],
    "hit_count": 6
  },
  "run_backtest.py": {
    "exists": true,
    "sha256": "8a85813936aa689cf6355b16f5ae4e30be97ebbcd962f5ac7ba3a1204a68fc6c",
    "hits": [],
    "hit_count": 0
  }
}
```

## Unresolved
```json
[
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
    "id": "full_115_artifact_missing_strategy_controls",
    "field": "strategy_controls",
    "blocking_for_replication": false
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
  },
  {
    "id": "full_115_artifact_missing_e1r_regime_wiring_enabled",
    "field": "e1r_regime_wiring_enabled",
    "blocking_for_replication": false
  },
  {
    "id": "full_115_artifact_missing_e1r_uptrend_execution_enabled",
    "field": "e1r_uptrend_execution_enabled",
    "blocking_for_replication": false
  }
]
```

## Validations
```json
{
  "artifact_recovery_complete": true,
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
  "strategy_files_unchanged": true,
  "k2_r9_loaded": true,
  "target_artifact_exists": true,
  "target_return_verified": true,
  "repository_grep_completed": true,
  "candidate_script_analysis_completed": true,
  "known_source_files_inspected": true,
  "generator_script_candidates_found": true,
  "target_artifact_has_market_gate_parameters": false,
  "target_artifact_has_regime_aware_logic": true,
  "target_artifact_has_sidecar_evidence": true,
  "blocking_unresolved_count": 6
}
```

## Decision
```json
{
  "k2_r9b_115_return_artifact_recovery_passed": true,
  "market_state_115_replication_ready": false,
  "formula_patch_allowed_now": false,
  "candidate_extraction_allowed_now": false,
  "implementation_may_resume": false,
  "unresolved": [
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
      "id": "full_115_artifact_missing_strategy_controls",
      "field": "strategy_controls",
      "blocking_for_replication": false
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
    },
    {
      "id": "full_115_artifact_missing_e1r_regime_wiring_enabled",
      "field": "e1r_regime_wiring_enabled",
      "blocking_for_replication": false
    },
    {
      "id": "full_115_artifact_missing_e1r_uptrend_execution_enabled",
      "field": "e1r_uptrend_execution_enabled",
      "blocking_for_replication": false
    }
  ],
  "next_required_stage_if_ready": "4C-2C-4E-ENGINE-K2-R10-MARKET_GATE_STANDALONE_REPLICATION_PROPOSAL",
  "next_required_stage_if_not_ready": "4C-2C-4E-ENGINE-K2-R9C-115_RETURN_GENERATOR_TRACE",
  "conclusion": "K2_R9B_RECOVERY_COMPLETE_NEEDS_GENERATOR_TRACE_OR_PARAM_EVIDENCE",
  "recommended_next_action": "If blocking unresolved remains, trace the generator script/call chain more narrowly and inspect the source lines that produced E1R_REGIME_AWARE_V0_2 and regime_aware_logic. Do not patch."
}
```
