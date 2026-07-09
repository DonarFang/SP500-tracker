# Stage 3.8E-2F-2C-4C-10F-4B-0 E1 vs E1R UPTREND Core Contract Audit

Generated At: `2026-07-09T08:47:35.245385+00:00`

## Status

- Status: `E1_E1R_UPTREND_CORE_CONTRACT_AUDIT_COMPLETE_NO_EXPORTS_WRITTEN`
- Strategy files unchanged: `True`
- Canonical existence unchanged: `True`
- Full backtest rerun: `False`

## Contract Assessment

```json
{
  "contract_conclusion": "UNCONFIRMED_DO_NOT_USE_E1_CORE_AS_E1R_CORE_CANONICAL_YET",
  "findings": [
    "E1 saved core row-derived total_return_pct is 89.8157%, while frozen E1R target total_return_pct is 116.7436%; delta=26.9279pp.",
    "Saved sidecar is active exactly 135 rows, all expected MA_CONFLICT/SIDEWAYS intervals.",
    "Source references core_variant_result / compose_e1r_v0_2_variant, so E1R appears to be composed from an explicit core result plus sidecar result.",
    "Source/result terms include e1r_uptrend_execution_enabled / e1r_candidates; this suggests E1R may have distinct execution instrumentation beyond plain E1.",
    "Found 18 metric/source candidate files that may contain frozen E1R/core contract evidence."
  ],
  "risk_flags": [
    "E1 core return differs materially from frozen E1R total return; sidecar alone must explain a large gap if E1 core is reused.",
    "E1R UPTREND core may not be identical to current exported E1 core unless the specific core_variant_result is recovered."
  ],
  "recommended_next_action": "Recover or regenerate the exact E1R core_variant_result / continuous core daily equity used by frozen E1R v0.2, then compare it against exports/e1_5y_backtest_equity_curve.json before any canonical E1R composition."
}
```

## E1 Saved Core Summary

```json
{
  "exists": true,
  "path": "exports/e1_5y_backtest_equity_curve.json",
  "artifact_type": "canonical_continuous_capital_e1_5y_core_equity_curve",
  "strategy_id": "E1_AUDITED_G4_MINHOLD10",
  "capital_model": "continuous_single_account",
  "row_count": 1259,
  "unique_dates": 1259,
  "date_start": "2021-06-11",
  "date_end": "2026-06-16",
  "first_equity": 100000.0,
  "last_equity": 189815.69,
  "total_return_pct_from_rows": 89.81569,
  "last_strategy_indexed": 189.81569000000002,
  "first_row_keys": [
    "cash",
    "daily_return",
    "daily_return_pct",
    "date",
    "equity",
    "market_state",
    "market_value",
    "n_positions",
    "portfolio_value",
    "source_row_keys",
    "strategy_indexed"
  ],
  "last_row_keys": [
    "cash",
    "daily_return",
    "daily_return_pct",
    "date",
    "equity",
    "market_state",
    "market_value",
    "n_positions",
    "portfolio_value",
    "source_row_keys",
    "strategy_indexed"
  ]
}
```

## Sidecar Saved Summary

```json
{
  "exists": true,
  "path": "exports/e1r_v0_2_sidecar_records_5y.json",
  "artifact_type": "e1r_v0_2_regime_aware_sidecar_records_5y",
  "row_count": 1260,
  "active_count": 135,
  "active_by_regime": {
    "SIDEWAYS": 135
  },
  "active_by_subclass": {
    "MA_CONFLICT": 135
  },
  "return_min": -0.012837265220872024,
  "return_max": 0.012239769727043218,
  "gross_exposure_min": 0.0,
  "gross_exposure_max": 0.25
}
```

## Metric Artifact Candidates

```json
[
  {
    "path": "docs/research/E1R_V0_2_STAGE3_8E2F1E0_TARGET_ACTION_INPUT_AUDIT.json",
    "score": 9,
    "matched_terms": [
      "116.7435999134756",
      "39.89942548515961",
      "E1R",
      "v0.2",
      "compose_e1r",
      "core_variant_result",
      "total_return_pct",
      "number_of_trades",
      "profit_factor"
    ],
    "size": 409256,
    "top_keys": [
      "data_files",
      "data_reports",
      "generated_at",
      "implementation_decision",
      "main",
      "next_stage",
      "policy",
      "question",
      "source_files",
      "source_reports",
      "stage",
      "status",
      "target_ready_candidate_files"
    ],
    "metric_like_values": {
      "status": "AUDIT_COMPLETE_NO_SOURCE_CHANGES"
    }
  },
  {
    "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C2_RECOVER_5Y_PORTFOLIO_EQUITY_CANDIDATES.json",
    "score": 9,
    "matched_terms": [
      "116.7435999134756",
      "39.89942548515961",
      "E1R",
      "v0.2",
      "compose_e1r",
      "core_variant_result",
      "total_return_pct",
      "number_of_trades",
      "profit_factor"
    ],
    "size": 806037,
    "top_keys": [
      "diagnosis",
      "exporter_hits",
      "generated_at",
      "inventory",
      "json_candidate_count",
      "policy",
      "preliminary_decision",
      "recommendation",
      "specific_files",
      "stage",
      "status",
      "text_hits",
      "top_e1_candidates",
      "top_e1r_candidates"
    ],
    "metric_like_values": {
      "status": "AUDIT_COMPLETE_NO_SOURCE_CHANGES"
    }
  },
  {
    "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C3_BACKTEST_GENERATOR_CANONICAL_EXPORT_PLAN.json",
    "score": 9,
    "matched_terms": [
      "116.7435999134756",
      "39.89942548515961",
      "E1R",
      "v0.2",
      "compose_e1r",
      "core_variant_result",
      "total_return_pct",
      "number_of_trades",
      "profit_factor"
    ],
    "size": 210496,
    "top_keys": [
      "canonical_export_plan",
      "diagnosis",
      "generated_at",
      "important_files",
      "json_summaries",
      "policy",
      "prior_4c2_summary",
      "stage",
      "status",
      "top_generator_candidates"
    ],
    "metric_like_values": {
      "status": "AUDIT_COMPLETE_PLAN_DEFINED_NO_SOURCE_CHANGES"
    }
  },
  {
    "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json",
    "score": 9,
    "matched_terms": [
      "116.7435999134756",
      "39.89942548515961",
      "E1R",
      "v0.2",
      "compose_e1r",
      "core_variant_result",
      "total_return_pct",
      "number_of_trades",
      "profit_factor"
    ],
    "size": 1028101,
    "top_keys": [
      "diagnosis",
      "discovered_json_candidates",
      "generated_at",
      "json_file_reports",
      "next_stage",
      "persisted_core_candidates",
      "persisted_interval_candidates",
      "persisted_sidecar_candidates",
      "policy",
      "real_source_probe",
      "source_file_reports",
      "stage",
      "status"
    ],
    "metric_like_values": {
      "status": "REAL_CORE_SIDECAR_RECORDS_AUDIT_COMPLETE_NO_EXPORTS_WRITTEN"
    }
  },
  {
    "path": "docs/research/E1R_V0_2_STAGE3_8E2F0_FORWARD_KICKOFF_AUDIT.json",
    "score": 8,
    "matched_terms": [
      "116.7435999134756",
      "39.89942548515961",
      "E1R",
      "v0.2",
      "compose_e1r",
      "total_return_pct",
      "number_of_trades",
      "profit_factor"
    ],
    "size": 137902,
    "top_keys": [
      "decision",
      "generated_at",
      "json_reports",
      "kickoff_schema",
      "main",
      "policy",
      "question",
      "readiness",
      "repo_candidate_files",
      "stage",
      "status",
      "watched_file_reports"
    ],
    "metric_like_values": {
      "status": "AUDIT_COMPLETE_NO_SOURCE_CHANGES"
    }
  },
  {
    "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C4_GENERATOR_INTERNALS_EXPORT_WRAPPER_PROTOTYPE.json",
    "score": 8,
    "matched_terms": [
      "116.7435999134756",
      "39.89942548515961",
      "E1R",
      "compose_e1r",
      "core_variant_result",
      "total_return_pct",
      "number_of_trades",
      "profit_factor"
    ],
    "size": 118151,
    "top_keys": [
      "diagnosis",
      "generated_at",
      "inspection",
      "policy",
      "prototype_wrapper_plan",
      "stage",
      "status",
      "toy_probe"
    ],
    "metric_like_values": {
      "status": "INSPECTION_COMPLETE_PROTOTYPE_PLAN_DEFINED_NO_SOURCE_CHANGES"
    }
  },
  {
    "path": "docs/research/E1R_V0_2_STAGE3_8E2A_DATA_SHAPE_AUDIT.json",
    "score": 7,
    "matched_terms": [
      "116.7435999134756",
      "39.89942548515961",
      "E1R",
      "v0.2",
      "total_return_pct",
      "number_of_trades",
      "profit_factor"
    ],
    "size": 442276,
    "top_keys": [
      "candidate_mapping",
      "export_reports",
      "exports_inspected",
      "generated_at",
      "main",
      "next_stage_options",
      "policy",
      "recommendations",
      "stage",
      "status"
    ],
    "metric_like_values": {
      "status": "AUDIT_COMPLETE_NO_DASHBOARD_SOURCE_CHANGES"
    }
  },
  {
    "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10E_R_CONTINUOUS_CAPITAL_CONTRACT.json",
    "score": 7,
    "matched_terms": [
      "E1R",
      "v0.2",
      "compose_e1r",
      "core_variant_result",
      "total_return_pct",
      "number_of_trades",
      "profit_factor"
    ],
    "size": 179768,
    "top_keys": [
      "canonical_existence_unchanged",
      "contract",
      "diagnosis",
      "full_5y_portfolio_candidates",
      "generated_at",
      "json_reports",
      "next_stage",
      "policy",
      "portfolio_curve_candidates",
      "source_function_heads",
      "source_reports",
      "stage",
      "status",
      "strategy_files_unchanged",
      "symbol_level_rejections"
    ],
    "metric_like_values": {
      "status": "CONTINUOUS_CAPITAL_CONTRACT_AUDIT_COMPLETE_NO_EXPORTS_WRITTEN"
    }
  },
  {
    "path": "docs/research/E1R_V0_2_OOS_SUMMARY_FIELD_AUDIT.json",
    "score": 6,
    "matched_terms": [
      "116.7435999134756",
      "39.89942548515961",
      "E1R",
      "v0.2",
      "total_return_pct",
      "profit_factor"
    ],
    "size": 57974,
    "top_keys": [
      "decision_rules",
      "generated_at",
      "main",
      "policy",
      "question",
      "readiness",
      "stage",
      "status",
      "target_reports",
      "targets"
    ],
    "metric_like_values": {
      "status": "AUDIT_COMPLETE_NO_SOURCE_CHANGES"
    }
  },
  {
    "path": "docs/research/E1R_V0_2_STAGE3_8E2F1A_FORWARD_SOURCE_AUDIT.json",
    "score": 6,
    "matched_terms": [
      "E1R",
      "v0.2",
      "compose_e1r",
      "core_variant_result",
      "total_return_pct",
      "profit_factor"
    ],
    "size": 284664,
    "top_keys": [
      "decision",
      "export_files",
      "export_reports",
      "generated_at",
      "main",
      "next_stage",
      "policy",
      "question",
      "roles",
      "source_files",
      "source_reports",
      "stage",
      "status"
    ],
    "metric_like_values": {
      "status": "AUDIT_COMPLETE_NO_SOURCE_CHANGES"
    }
  },
  {
    "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C3FB_TREND_REGIME_SOURCE_AUDIT.json",
    "score": 6,
    "matched_terms": [
      "E1R",
      "v0.2",
      "compose_e1r",
      "total_return_pct",
      "number_of_trades",
      "profit_factor"
    ],
    "size": 121529,
    "top_keys": [
      "candidate_source_files",
      "diagnosis",
      "export_summaries",
      "generated_at",
      "next_patch_should",
      "policy",
      "search_terms",
      "stage",
      "status",
      "workflow_hits"
    ],
    "metric_like_values": {
      "status": "AUDIT_COMPLETE_NO_SOURCE_CHANGES"
    }
  },
  {
    "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10A_DIRECT_GENERATOR_FUNCTION_AUDIT.json",
    "score": 6,
    "matched_terms": [
      "E1R",
      "v0.2",
      "compose_e1r",
      "core_variant_result",
      "total_return_pct",
      "profit_factor"
    ],
    "size": 323785,
    "top_keys": [
      "composer_function_candidates",
      "diagnosis",
      "generated_at",
      "import_probe",
      "next_stage",
      "policy",
      "sidecar_function_candidates",
      "stage",
      "status",
      "target_reports"
    ],
    "metric_like_values": {
      "status": "DIRECT_GENERATOR_FUNCTION_AUDIT_COMPLETE_NO_EXPORTS_WRITTEN"
    }
  },
  {
    "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C1_5Y_EQUITY_ARTIFACT_AUDIT.json",
    "score": 6,
    "matched_terms": [
      "E1R",
      "v0.2",
      "compose_e1r",
      "total_return_pct",
      "number_of_trades",
      "profit_factor"
    ],
    "size": 63783,
    "top_keys": [
      "candidate_count",
      "diagnosis",
      "generated_at",
      "known_summaries",
      "policy",
      "portfolio_candidates_count",
      "recommendation",
      "script_hits",
      "stage",
      "status",
      "top_e1_candidates",
      "top_e1r_candidates"
    ],
    "metric_like_values": {
      "status": "AUDIT_COMPLETE_NO_SOURCE_CHANGES"
    }
  },
  {
    "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C6_INTERVAL_SCHEMA_SOURCE_AUDIT.json",
    "score": 6,
    "matched_terms": [
      "E1R",
      "v0.2",
      "core_variant_result",
      "total_return_pct",
      "number_of_trades",
      "profit_factor"
    ],
    "size": 212484,
    "top_keys": [
      "candidate_json_summaries",
      "diagnosis",
      "exact_schema_probe",
      "function_sources",
      "generated_at",
      "grep_results",
      "next_stage",
      "policy",
      "schema_candidates",
      "stage",
      "status"
    ],
    "metric_like_values": {
      "status": "INTERVAL_SCHEMA_AUDIT_COMPLETE_NO_EXPORTS_WRITTEN"
    }
  },
  {
    "path": "docs/research/E1R_V0_2_STAGE3_8A_DASHBOARD_REFACTOR_AUDIT.json",
    "score": 5,
    "matched_terms": [
      "E1R",
      "v0.2",
      "total_return_pct",
      "number_of_trades",
      "profit_factor"
    ],
    "size": 37000,
    "top_keys": [
      "acceptance_criteria_for_stage_3_8b",
      "current_dashboard",
      "data_source_map",
      "desired_research_page_structure",
      "export_summaries",
      "files_inspected",
      "generated_at",
      "main",
      "next_stage",
      "policy",
      "recommended_stage_3_8b_actions",
      "refactor_risks",
      "remove_or_hide_targets",
      "stage",
      "status"
    ],
    "metric_like_values": {
      "status": "AUDIT_COMPLETE_NO_SOURCE_CHANGES"
    }
  },
  {
    "path": "docs/research/E1R_V0_2_STAGE3_8D_NATIVE_RENDER_AUDIT.json",
    "score": 5,
    "matched_terms": [
      "E1R",
      "v0.2",
      "total_return_pct",
      "number_of_trades",
      "profit_factor"
    ],
    "size": 220109,
    "top_keys": [
      "all_function_names_sample",
      "app_overview",
      "app_target_term_hits",
      "css_target_term_hits",
      "export_references",
      "export_summaries",
      "files_inspected",
      "generated_at",
      "high_interest_functions",
      "index_tab_hits",
      "key_neighborhoods",
      "likely_render_functions",
      "main",
      "next_stage",
      "policy",
      "restore_status",
      "stage",
      "stage_3_8e_acceptance_criteria",
      "stage_3_8e_recommendations",
      "status"
    ],
    "metric_like_values": {
      "status": "AUDIT_COMPLETE_NO_DASHBOARD_SOURCE_CHANGES"
    }
  },
  {
    "path": "docs/research/E1R_V0_2_STAGE3_8E2F1G0_SUMMARY_MAPPING_AUDIT.json",
    "score": 5,
    "matched_terms": [
      "E1R",
      "v0.2",
      "total_return_pct",
      "number_of_trades",
      "profit_factor"
    ],
    "size": 14594,
    "top_keys": [
      "dashboard_mentions_forward_fields",
      "forward_summary_field_presence",
      "generated_at",
      "json_reports",
      "main",
      "next_stage",
      "policy",
      "recommended_summary_fields",
      "stage",
      "status",
      "summary_mapping_readiness",
      "text_reports"
    ],
    "metric_like_values": {
      "status": "AUDIT_COMPLETE_NO_SOURCE_CHANGES"
    }
  },
  {
    "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F3D_E1_CANONICAL_INTEGRITY_AUDIT.json",
    "score": 5,
    "matched_terms": [
      "E1R",
      "e1r_candidate_count",
      "total_return_pct",
      "number_of_trades",
      "profit_factor"
    ],
    "size": 7463,
    "top_keys": [
      "canonical_audit",
      "diagnosis",
      "generated_at",
      "next_stage",
      "patch_report",
      "policy",
      "source_report_audit",
      "stage",
      "status",
      "strategy_files_unchanged"
    ],
    "metric_like_values": {
      "status": "E1_CANONICAL_INTEGRITY_AUDIT_COMPLETE_MAPPING_FIXED_NO_BACKTEST"
    }
  },
  {
    "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C8_DRY_RUN_GENERATION_PATH_AUDIT.json",
    "score": 5,
    "matched_terms": [
      "116.7435999134756",
      "39.89942548515961",
      "E1R",
      "total_return_pct",
      "profit_factor"
    ],
    "size": 9646,
    "top_keys": [
      "diagnosis",
      "generated_at",
      "next_stage",
      "policy",
      "stage",
      "status",
      "summary",
      "wrapper_output"
    ],
    "metric_like_values": {
      "status": "DRY_RUN_GENERATION_PATH_AUDIT_COMPLETE_NO_CANONICAL_EXPORTS_WRITTEN"
    },
    "summary_keys": [
      "attempt_count",
      "can_generate_from_persisted_inputs",
      "core_sources_count",
      "decision",
      "frozen_metric_targets",
      "ok_nonempty_attempt_count",
      "sidecar_sources_count"
    ],
    "summary_metric_like_values": {}
  },
  {
    "path": "exports/e1r_v0_2_backtest_summary.json",
    "score": 5,
    "matched_terms": [
      "116.7435999134756",
      "39.89942548515961",
      "E1R",
      "total_return_pct",
      "profit_factor"
    ],
    "size": 941,
    "top_keys": [
      "alpha_pct",
      "artifact_type",
      "composition_exists",
      "frozen_artifact",
      "max_drawdown_pct",
      "profit_factor",
      "regeneration_note",
      "regime_aware_logic",
      "research_status",
      "row_count",
      "sharpe_ratio",
      "sidecar_active_by_regime",
      "sidecar_active_by_subclass",
      "sidecar_active_days",
      "source_file",
      "source_json_path",
      "spx_return_pct",
      "strategy_id",
      "total_return_pct",
      "variant"
    ],
    "metric_like_values": {
      "strategy_id": "E1R_REGIME_AWARE_V0_2",
      "total_return_pct": 116.7435999134756,
      "spx_return_pct": 76.844174428316,
      "alpha_pct": 39.89942548515961,
      "max_drawdown_pct": 25.904809362815108,
      "profit_factor": 1.1919630955509348,
      "sharpe_ratio": 0.7957270568329264
    }
  },
  {
    "path": "data/research/e1r/e1r_formal_backtest_v0_1.json",
    "score": 4,
    "matched_terms": [
      "E1R",
      "total_return_pct",
      "number_of_trades",
      "profit_factor"
    ],
    "size": 81365,
    "top_keys": [
      "comparison_base",
      "e1_metrics",
      "equity_curve",
      "metrics",
      "source",
      "spx_curve",
      "status",
      "trades",
      "variant_id"
    ],
    "metric_like_values": {
      "status": "FORMAL_BACKTEST_AVAILABLE_RESEARCH_EXPORT"
    },
    "metrics_keys": [
      "alpha_pct",
      "avg_holding_days",
      "exposure_pct",
      "max_drawdown_pct",
      "number_of_trades",
      "profit_factor",
      "sharpe_ratio",
      "spx_total_return_pct",
      "total_return_pct",
      "win_rate_pct"
    ],
    "metrics_metric_like_values": {
      "total_return_pct": 65.71,
      "alpha_pct": -3.65,
      "max_drawdown_pct": 32.35,
      "profit_factor": 1.97,
      "sharpe_ratio": 0.58,
      "number_of_trades": 39
    }
  },
  {
    "path": "data/research/e1r/e1r_phase3e_confirmed_quality_diagnostic.json",
    "score": 4,
    "matched_terms": [
      "E1R",
      "total_return_pct",
      "number_of_trades",
      "profit_factor"
    ],
    "size": 32036,
    "top_keys": [
      "confirmed_trade_count",
      "confirmed_trade_stats",
      "e1_trade_stats_reference",
      "entry_month_concentration",
      "entry_type_counts",
      "fairness_controls",
      "generated_at",
      "inputs",
      "phase3c_reference",
      "portfolio_summary",
      "quality_grade",
      "regime_gap_from_review",
      "sector_concentration",
      "sim_end_sensitivity",
      "status",
      "symbol_concentration",
      "top_winner_concentration",
      "top_winners",
      "worst_losers"
    ],
    "metric_like_values": {
      "status": "DIAGNOSTIC_ONLY_NO_TRADING_LOGIC_CHANGE"
    }
  },
  {
    "path": "data/research/e1r/e1r_regime_attribution_review.json",
    "score": 4,
    "matched_terms": [
      "E1R",
      "total_return_pct",
      "number_of_trades",
      "profit_factor"
    ],
    "size": 11929,
    "top_keys": [
      "backtest_source",
      "comparison",
      "fairness_controls",
      "generated_at",
      "regime_source",
      "shared_days",
      "shared_regime_day_counts",
      "shared_window_end",
      "shared_window_start",
      "status",
      "strategies",
      "strategy_ids",
      "trade_review"
    ],
    "metric_like_values": {
      "status": "DIAGNOSTIC_ONLY_NO_TRADING_LOGIC_CHANGE"
    }
  },
  {
    "path": "docs/research/E1R_V0_2_STAGE3_2_BACKTEST_INTEGRATION_REPORT.json",
    "score": 4,
    "matched_terms": [
      "E1R",
      "v0.2",
      "compose_e1r",
      "profit_factor"
    ],
    "size": 2413,
    "top_keys": [
      "boundary",
      "composer_functions_available",
      "composer_functions_used_after_integration",
      "composer_functions_used_by_feature_backtest",
      "diff_file",
      "feature",
      "feature_e1r_hits",
      "feature_legacy_hits",
      "generated_at",
      "integrated_e1r_hits",
      "integrated_file",
      "integrated_legacy_hits",
      "line_counts",
      "main",
      "main_before_legacy_hits",
      "next_stage",
      "policy",
      "required_e1r_markers",
      "required_legacy_markers",
      "snapshots",
      "stage",
      "status"
    ],
    "metric_like_values": {
      "status": "INTEGRATED_FEATURE_BACKTEST_WITH_GUARDS"
    }
  },
  {
    "path": "docs/research/E1R_V0_2_STAGE3_5_DEPENDENCY_FIX_REPORT.json",
    "score": 4,
    "matched_terms": [
      "E1R",
      "v0.2",
      "total_return_pct",
      "profit_factor"
    ],
    "size": 7669,
    "top_keys": [
      "backtest_json_mutation",
      "boundary",
      "copied_frozen_backtest_artifacts",
      "copied_research_dependency_dir",
      "copied_research_file_count",
      "copied_research_files_sample",
      "feature",
      "generated_at",
      "main",
      "reason",
      "selected_equity_source",
      "selected_summary_source",
      "source_code_patch",
      "stage",
      "status"
    ],
    "metric_like_values": {
      "status": "DEPENDENCIES_READY_WITH_DISCOVERED_FROZEN_BACKTEST_ARTIFACTS"
    }
  },
  {
    "path": "docs/research/E1R_V0_2_STAGE3_5_MAIN_SMOKE_TEST_REPORT.json",
    "score": 4,
    "matched_terms": [
      "E1R",
      "v0.2",
      "total_return_pct",
      "profit_factor"
    ],
    "size": 11826,
    "top_keys": [
      "dashboard_checks",
      "dependency_fix",
      "export_commands",
      "exports",
      "generated_at",
      "main",
      "py_compile",
      "skipped_commands",
      "stage",
      "status",
      "summary",
      "workflow_checks"
    ],
    "metric_like_values": {
      "status": "PASS_WITH_DISCOVERED_FROZEN_BACKTEST_ARTIFACTS"
    },
    "summary_keys": [
      "dashboard_json_references_validated",
      "exports_validated",
      "frozen_backtest_artifacts_validated",
      "oos_export_commands_passed",
      "py_compile_passed",
      "ready_for_manual_dashboard_review"
    ],
    "summary_metric_like_values": {}
  },
  {
    "path": "docs/research/E1R_V0_2_STAGE3_8E2B_STRUCTURAL_DIFF_AUDIT.json",
    "score": 4,
    "matched_terms": [
      "E1R",
      "total_return_pct",
      "number_of_trades",
      "profit_factor"
    ],
    "size": 61857,
    "top_keys": [
      "after_summary_block",
      "function_ranges",
      "generated_at",
      "high_risk_removed_contexts",
      "interpretation",
      "main",
      "next_options",
      "old_e1_cards_removed",
      "old_e1_header_block_analysis",
      "policy",
      "removed_line_summary",
      "removed_non_ui_candidates_in_renderE1RResearchPanel",
      "removed_non_ui_candidates_in_render_tab",
      "scope",
      "stage",
      "status",
      "symbol_drops",
      "symbol_report"
    ],
    "metric_like_values": {
      "status": "AUDIT_COMPLETE_NO_SOURCE_CHANGES"
    }
  },
  {
    "path": "docs/research/E1R_V0_2_STAGE3_8E2B_V3_PREPATCH_AUDIT.json",
    "score": 4,
    "matched_terms": [
      "E1R",
      "total_return_pct",
      "number_of_trades",
      "profit_factor"
    ],
    "size": 12049,
    "top_keys": [
      "generated_at",
      "main",
      "next_patch_rules",
      "next_stage",
      "policy",
      "stage",
      "status",
      "targets"
    ],
    "metric_like_values": {
      "status": "AUDIT_COMPLETE_NO_SOURCE_CHANGES"
    }
  },
  {
    "path": "docs/research/E1R_V0_2_STAGE3_8E2B_V4_SURGICAL_MAP.json",
    "score": 4,
    "matched_terms": [
      "E1R",
      "total_return_pct",
      "number_of_trades",
      "profit_factor"
    ],
    "size": 45256,
    "top_keys": [
      "generated_at",
      "keep_logic_lines",
      "main",
      "policy",
      "recommended_patch_rule",
      "replaceable_ui_candidate_lines",
      "section",
      "section_range",
      "stage",
      "status",
      "summary",
      "template_blocks"
    ],
    "metric_like_values": {
      "status": "AUDIT_COMPLETE_NO_SOURCE_CHANGES"
    },
    "summary_keys": [
      "keep_logic_line_count",
      "replaceable_ui_candidate_line_count",
      "template_block_count"
    ],
    "summary_metric_like_values": {}
  },
  {
    "path": "docs/research/E1R_V0_2_STAGE3_8E2F1B_FORWARD_IMPLEMENTATION_PLAN.json",
    "score": 4,
    "matched_terms": [
      "E1R",
      "v0.2",
      "number_of_trades",
      "profit_factor"
    ],
    "size": 10732,
    "top_keys": [
      "acceptance_for_this_stage",
      "current_exports",
      "decision",
      "files_not_to_modify_in_implementation",
      "generated_at",
      "implementation_phases",
      "kickoff_policy",
      "main",
      "policy",
      "proposed_files_to_add",
      "proposed_files_to_modify",
      "risk_controls",
      "source_audit_basis",
      "stage",
      "status",
      "target_schema"
    ],
    "metric_like_values": {
      "status": "PLAN_COMPLETE_NO_ENGINE_CHANGES"
    }
  },
  {
    "path": "docs/research/E1R_V0_2_STAGE3_8E2F1C_RUNNER_DRY_RUN_AUDIT.json",
    "score": 4,
    "matched_terms": [
      "E1R",
      "v0.2",
      "total_return_pct",
      "profit_factor"
    ],
    "size": 35295,
    "top_keys": [
      "after_hashes",
      "before_hashes",
      "changed_watch_files",
      "classification",
      "decision_rules",
      "generated_at",
      "git_status_after_script_run",
      "json_after",
      "main",
      "policy",
      "script_results",
      "scripts",
      "stage",
      "status",
      "watch_files"
    ],
    "metric_like_values": {
      "status": "AUDIT_COMPLETE_EXPORT_CHANGES_REVERTED"
    }
  },
  {
    "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C3A_TRADE_LOG_RENDER_PATH_AUDIT.json",
    "score": 4,
    "matched_terms": [
      "E1R",
      "v0.2",
      "number_of_trades",
      "profit_factor"
    ],
    "size": 10847,
    "top_keys": [
      "app_report",
      "generated_at",
      "json_reports",
      "main",
      "next_stage",
      "policy",
      "readiness",
      "recommended_patch",
      "stage",
      "status"
    ],
    "metric_like_values": {
      "status": "AUDIT_COMPLETE_NO_SOURCE_CHANGES"
    }
  },
  {
    "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C3FD_MARKET_STATE_GENERATOR_AUDIT.json",
    "score": 4,
    "matched_terms": [
      "E1R",
      "v0.2",
      "number_of_trades",
      "profit_factor"
    ],
    "size": 335454,
    
```

## Key Source Hits

```json
{
  "src/engine/backtest.py": [
    {
      "path": "src/engine/backtest.py",
      "line": 79,
      "terms": [
        "ls60"
      ],
      "context": [
        {
          "line": 77,
          "text": "    \"block_add_after_take_profit\": False,"
        },
        {
          "line": 78,
          "text": "    \"version\":           \"1.6-top3-rs95-minhold-relstop-comparison\","
        },
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
        }
      ]
    },
    {
      "path": "src/engine/backtest.py",
      "line": 763,
      "terms": [
        "run_stateful_simulation"
      ],
      "context": [
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
        }
      ]
    },
    {
      "path": "src/engine/backtest.py",
      "line": 805,
      "terms": [
        "e1r_uptrend_execution_enabled"
      ],
      "context": [
        {
          "line": 803,
          "text": "    e1r_shell_mode = bool(a.get(\"e1r_shell_mode\", False))"
        },
        {
          "line": 804,
          "text": "    e1r_regime_wiring_enabled = bool(a.get(\"e1r_regime_wiring_enabled\", False))"
        },
        {
          "line": 805,
          "text": "    e1r_uptrend_execution_enabled = bool(a.get(\"e1r_uptrend_execution_enabled\", False))"
        },
        {
          "line": 806,
          "text": "    e1r_regime_daily = a.get(\"e1r_regime_daily\", {}) or {}"
        },
        {
          "line": 807,
          "text": ""
        }
      ]
    },
    {
      "path": "src/engine/backtest.py",
      "line": 819,
      "terms": [
        "UPTREND"
      ],
      "context": [
        {
          "line": 817,
          "text": ""
        },
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
        }
      ]
    },
    {
      "path": "src/engine/backtest.py",
      "line": 820,
      "terms": [
        "UPTREND"
      ],
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
        }
      ]
    },
    {
      "path": "src/engine/backtest.py",
      "line": 821,
      "terms": [
        "SIDEWAYS"
      ],
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
        }
      ]
    },
    {
      "path": "src/engine/backtest.py",
      "line": 822,
      "terms": [
        "SIDEWAYS"
      ],
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
        }
      ]
    },
    {
      "path": "src/engine/backtest.py",
      "line": 830,
      "terms": [
        "UPTREND"
      ],
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
        }
      ]
    },
    {
      "path": "src/engine/backtest.py",
      "line": 831,
      "terms": [
        "UPTREND"
      ],
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
        }
      ]
    },
    {
      "path": "src/engine/backtest.py",
      "line": 832,
      "terms": [
        "SIDEWAYS"
      ],
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
        }
      ]
    },
    {
      "path": "src/engine/backtest.py",
      "line": 833,
      "terms": [
        "SIDEWAYS"
      ],
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
        }
      ]
    },
    {
      "path": "src/engine/backtest.py",
      "line": 849,
      "terms": [
        "ls60"
      ],
      "context": [
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
      "path": "src/engine/backtest.py",
      "line": 894,
      "terms": [
        "ls60"
      ],
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
        }
      ]
    },
    {
      "path": "src/engine/backtest.py",
      "line": 895,
      "terms": [
        "ls60"
      ],
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
        }
      ]
    },
    {
      "path": "src/engine/backtest.py",
      "line": 934,
      "terms": [
        "LS60",
        "ls60"
      ],
      "context": [
        {
          "line": 932,
          "text": "                f\"RelStop={'ON' if relative_stop_enabled else 'OFF'} \""
        },
        {
          "line": 933,
          "text": "                f\"({relative_stop_underperform*100:.1f}% vs SPX)\")"
        },
        {
          "line": 934,
          "text": "    logger.info(f\"  LS60 mode: {ls60_exit_mode} \""
        },
        {
          "line": 935,
          "text": "                f\"({'LS<60 → EXIT' if ls60_exit_mode == 'exit' else 'LS<60 → REDUCE'})\")"
        },
        {
          "line": 936,
          "text": "    logger.info(f\"  ── Param check: ls60={ls60_exit_mode} rs={entry_rs_min} \""
        }
      ]
    },
    {
      "path": "src/engine/backtest.py",
      "line": 935,
      "terms": [
        "ls60"
      ],
      "context": [
        {
          "line": 933,
          "text": "                f\"({relative_stop_underperform*100:.1f}% vs SPX)\")"
        },
        {
          "line": 934,
          "text": "    logger.info(f\"  LS60 mode: {ls60_exit_mode} \""
        },
        {
          "line": 935,
          "text": "                f\"({'LS<60 → EXIT' if ls60_exit_mode == 'exit' else 'LS<60 → REDUCE'})\")"
        },
        {
          "line": 936,
          "text": "    logger.info(f\"  ── Param check: ls60={ls60_exit_mode} rs={entry_rs_min} \""
        },
        {
          "line": 937,
          "text": "                f\"top_n={entry_top_n} minhold={min_holding_days} \""
        }
      ]
    },
    {
      "path": "src/engine/backtest.py",
      "line": 936,
      "terms": [
        "ls60"
      ],
      "context": [
        {
          "line": 934,
          "text": "    logger.info(f\"  LS60 mode: {ls60_exit_mode} \""
        },
        {
          "line": 935,
          "text": "                f\"({'LS<60 → EXIT' if ls60_exit_mode == 'exit' else 'LS<60 → REDUCE'})\")"
        },
        {
          "line": 936,
          "text": "    logger.info(f\"  ── Param check: ls60={ls60_exit_mode} rs={entry_rs_min} \""
        },
        {
          "line": 937,
          "text": "                f\"top_n={entry_top_n} minhold={min_holding_days} \""
        },
        {
          "line": 938,
          "text": "                f\"relstop={relative_stop_enabled} gate={market_gate_enabled} ──\")"
        }
      ]
    },
    {
      "path": "src/engine/backtest.py",
      "line": 1045,
      "terms": [
        "ls60"
      ],
      "context": [
        {
          "line": 1043,
          "text": "        \"dynamic_hard_exit_triggered\":     0,  # E2: 硬退出触发次数"
        },
        {
          "line": 1044,
          "text": "        \"dynamic_soft_exit_confirmed\":     0,  # E2: 软退出确认次数"
        },
        {
          "line": 1045,
          "text": "        \"ls60_reduce_already_triggered\":   0,"
        },
        {
          "line": 1046,
          "text": "        \"action_reason_buy_add_mismatch\":  0,   # BUY/ADD 不一致（记录，不中断）"
        },
        {
          "line": 1047,
          "text": "        \"fill_only_no_empty_slot\":         0,   # fill_only 模式：无空仓位，跳过 BUY"
        }
      ]
    },
    {
      "path": "src/engine/backtest.py",
      "line": 1188,
      "terms": [
        "ls60"
      ],
      "context": [
        {
          "line": 1186,
          "text": "                        \"realized_cost_basis\":   0.0,"
        },
        {
          "line": 1187,
          "text": "                        \"action_history\":        [\"BUY\"],"
        },
        {
          "line": 1188,
          "text": "                        \"ls60_reduce_triggered\": False,  # 方案A：LS<60 REDUCE 一次性保护"
        },
        {
          "line": 1189,
          "text": "                        # E1-R Phase 2 regime wiring telemetry. Observer-only."
        },
        {
          "line": 1190,
          "text": "                        \"entry_regime\": _e1r_regime_on(exec_date),"
        }
      ]
    },
    {
      "path": "src/engine/backtest.py",
      "line": 1191,
      "terms": [
        "E1R"
      ],
      "context": [
        {
          "line": 1189,
          "text": "                        # E1-R Phase 2 regime wiring telemetry. Observer-only."
        },
        {
          "line": 1190,
          "text": "                        \"entry_regime\": _e1r_regime_on(exec_date),"
        },
        {
          "line": 1191,
          "text": "                        \"entry_type\": order.get(\"e1r_entry_type\") or (\"E1R_PLACEHOLDER_LEGACY_ENTRY\" if e1r_regime_wiring_enabled else None),"
        },
        {
          "line": 1192,
          "text": "                        \"regime_day_weights\": {},"
        },
        {
          "line": 1193,
          "text": "                    }"
        }
      ]
    },
    {
      "path": "src/engine/backtest.py",
      "line": 1222,
      "terms": [
        "e1r_uptrend_execution_enabled"
      ],
      "context": [
        {
          "line": 1220,
          "text": "                    h[\"avg_cost\"]   = (old_s * old_c + add_shares * exec_price) / (old_s + add_shares)"
        },
        {
          "line": 1221,
          "text": "                    h[\"shares\"]    += add_shares"
        },
        {
          "line": 1222,
          "text": "                    h[\"size_units\"] = min(1.0 if e1r_uptrend_execution_enabled else 1.5, h[\"size_units\"] + _add_size_units)"
        },
        {
          "line": 1223,
          "text": "                    if order.get(\"e1r_entry_type\"):"
        },
        {
          "line": 1224,
          "text": "                        h[\"e1r_entry_type\"] = order.get(\"e1r_entry_type\")"
        }
      ]
    },
    {
      "path": "src/engine/backtest.py",
      "line": 1227,
      "terms": [
        "ls60"
      ],
      "context": [
        {
          "line": 1225,
          "text": "                        h[\"entry_type\"] = order.get(\"e1r_entry_type\")"
        },
        {
          "line": 1226,
          "text": "                    h[\"action_history\"].append(\"ADD\")"
        },
        {
          "line": 1227,
          "text": "                    h[\"ls60_reduce_triggered\"] = False  # ADD 后清零 ls60 保护"
        },
        {
          "line": 1228,
          "text": "                    cash -= target_add"
        },
        {
          "line": 1229,
          "text": "                    orders_executed += 1"
        }
      ]
    },
    {
      "path": "src/engine/backtest.py",
      "line": 1333,
      "terms": [
        "ls60"
      ],
      "context": [
        {
          "line": 1331,
          "text": "                        h[\"relative_stop_exec_date\"] = exec_date"
        },
        {
          "line": 1332,
          "text": "                        relative_stop_stats[\"executed\"] += 1"
        },
        {
          "line": 1333,
          "text": "                    # 记录 REDUCE 原因，并设置 ls60 一次性保护"
        },
        {
          "line": 1334,
          "text": "                    reduce_primary = order.get(\"primary_reason\", \"\")"
        },
        {
          "line": 1335,
          "text": "                    if reduce_primary:"
        }
      ]
    },
    {
      "path": "src/engine/backtest.py",
      "line": 1338,
      "terms": [
        "ls60"
      ],
      "context": [
        {
          "line": 1336,
          "text": "                        executed_reduce_reason_dist[reduce_primary] =                             executed_reduce_reason_dist.get(reduce_primary, 0) + 1"
        },
        {
          "line": 1337,
          "text": "                    if reduce_primary == \"leader_score_below_60\":"
        },
        {
          "line": 1338,
          "text": "                        h[\"ls60_reduce_triggered\"] = True"
        },
        {
          "line": 1339,
          "text": "                    orders_executed += 1"
        },
        {
          "line": 1340,
          "text": ""
        }
      ]
    },
    {
      "path": "src/engine/backtest.py",
      "line": 1586,
      "terms": [
        "ls60"
      ],
      "context": [
        {
          "line": 1584,
          "text": "                state, mom, rs, close_t, ma50_v, ma50_sl,"
        },
        {
          "line": 1585,
          "text": "                ls, th, market_score_default,"
        },
        {
          "line": 1586,
          "text": "                ls60_exit_mode=ls60_exit_mode,"
        },
        {
          "line": 1587,
          "text": "            )"
        },
        {
          "line": 1588,
          "text": ""
        }
      ]
    },
    {
      "path": "src/engine/backtest.py",
      "line": 1621,
      "terms": [
        "UPTREND"
      ],
      "context": [
        {
          "line": 1619,
          "text": "        )"
        },
        {
          "line": 1620,
          "text": ""
        },
        {
          "line": 1621,
          "text": "        # E1-R Phase 3A: UPTREND candidate tagging only."
        },
        {
          "line": 1622,
          "text": "        # This does not change buy_orders, management_orders, holdings, or cash."
        },
        {
          "line": 1623,
          "text": "        if e1r_shell_mode and e1r_regime_wiring_enabled and _e1r_regime_on(date_t) == \"UPTREND\":"
        }
      ]
    },
    {
      "path": "src/engine/backtest.py",
      "line": 1623,
      "terms": [
        "UPTREND"
      ],
      "context": [
        {
          "line": 1621,
          "text": "        # E1-R Phase 3A: UPTREND candidate tagging only."
        },
        {
          "line": 1622,
          "text": "        # This does not change buy_orders, management_orders, holdings, or cash."
        },
        {
          "line": 1623,
          "text": "        if e1r_shell_mode and e1r_regime_wiring_enabled and _e1r_regime_on(date_t) == \"UPTREND\":"
        },
        {
          "line": 1624,
          "text": "            leader_rank_all = {s: i + 1 for i, (s, _) in enumerate(top_ranked)}"
        },
        {
          "line": 1625,
          "text": "            for sym, sig in day_signals.items():"
        }
      ]
    },
    {
      "path": "src/engine/backtest.py",
      "line": 1665,
      "terms": [
        "E1R",
        "UPTREND"
      ],
      "context": [
        {
          "line": 1663,
          "text": "                )"
        },
        {
          "line": 1664,
          "text": "                if emerging or confirmed:"
        },
        {
          "line": 1665,
          "text": "                    entry_type = \"E1R_UPTREND_CONFIRMED\" if confirmed else \"E1R_UPTREND_EMERGING\""
        },
        {
          "line": 1666,
          "text": "                    reasons = confirmed_reasons if confirmed else emerging_reasons"
        },
        {
          "line": 1667,
          "text": "                    sig[\"e1r_entry_type\"] = entry_type"
        }
      ]
    },
    {
      "path": "src/engine/backtest.py",
      "line": 1674,
      "terms": [
        "UPTREND"
      ],
      "context": [
        {
          "line": 1672,
          "text": "                        \"date\": date_t,"
        },
        {
          "line": 1673,
          "text": "                        \"symbol\": sym,"
        },
        {
          "line": 1674,
          "text": "                        \"spx_regime\": \"UPTREND\","
        },
        {
          "line": 1675,
          "text": "                        \"e1r_entry_type\": entry_type,"
        },
        {
          "line": 1676,
          "text": "                        \"e1r_uptrend_emerging_eligible\": emerging,"
        }
      ]
    },
    {
      "path": "src/engine/backtest.py",
      "line": 1695,
      "terms": [
        "UPTREND"
      ],
      "context": [
        {
          "line": 1693,
          "text": "                    })"
        },
        {
          "line": 1694,
          "text": ""
        },
        {
          "line": 1695,
          "text": "        # E1-R Phase 3B: UPTREND Execution v0.1 candidate selection."
        },
        {
          "line": 1696,
          "text": "        # Only entry execution is changed; existing E1 reduce/exit logic remains intact."
        },
        {
          "line": 1697,
          "text": "        e1r_selected_buy: dict | None = None"
        }
      ]
    },
    {
      "path": "src/engine/backtest.py",
      "line": 1698,
      "terms": [
        "e1r_uptrend_execution_enabled",
        "UPTREND"
      ],
      "context": [
        {
          "line": 1696,
          "text": "        # Only entry execution is changed; existing E1 reduce/exit logic remains intact."
        },
        {
          "line": 1697,
          "text": "        e1r_selected_buy: dict | None = None"
        },
        {
          "line": 1698,
          "text": "        if e1r_uptrend_execution_enabled and _e1r_regime_on(date_t) == \"UPTREND\":"
        },
        {
          "line": 1699,
          "text": "            e1r_buy_candidates = []"
        },
        {
          "line": 1700,
          "text": "            for s, v in day_signals.items():"
        }
      ]
    },
    {
      "path": "src/engine/backtest.py",
      "line": 1706,
      "terms": [
        "E1R",
        "UPTREND"
      ],
      "context": [
        {
          "line": 1704,
          "text": "                    continue"
        },
        {
          "line": 1705,
          "text": "                _etype = v.get(\"e1r_entry_type\")"
        },
        {
          "line": 1706,
          "text": "                _priority = 0 if _etype == \"E1R_UPTREND_CONFIRMED\" else 1"
        },
        {
          "line": 1707,
          "text": "                e1r_buy_candidates.append(("
        },
        {
          "line": 1708,
          "text": "                    _priority,"
        }
      ]
    },
    {
      "path": "src/engine/backtest.py",
      "line": 1725,
      "terms": [
        "E1R",
        "UPTREND"
      ],
      "context": [
        {
          "line": 1723,
          "text": "                        \"sig\": _sig,"
        },
        {
          "line": 1724,
          "text": "                        \"entry_type\": _etype,"
        },
        {
          "line": 1725,
          "text": "                        \"target_size_units\": 1.0 if _etype == \"E1R_UPTREND_CONFIRMED\" else 0.5,"
        },
        {
          "line": 1726,
          "text": "                    }"
        },
        {
          "line": 1727,
          "text": "                else:"
        }
      ]
    },
    {
      "path": "src/engine/backtest.py",
      "line": 1783,
      "terms": [
        "e1r_uptrend_execution_enabled"
      ],
      "context": [
        {
          "line": 1781,
          "text": "            #   Position Mgmt → 由 trade_action 决定（HOLD/ADD/REDUCE/EXIT）"
        },
        {
          "line": 1782,
          "text": "            if ("
        },
        {
          "line": 1783,
          "text": "                e1r_uptrend_execution_enabled"
        },
        {
          "line": 1784,
          "text": "                and e1r_selected_buy"
        },
        {
          "line": 1785,
          "text": "                and sym == e1r_selected_buy[\"sym\"]"
        }
      ]
    },
    {
      "path": "src/engine/backtest.py",
      "line": 1796,
      "terms": [
        "E1R",
        "UPTREND"
      ],
      "context": [
        {
          "line": 1794,
          "text": "                    \"close_t\":        close_t,"
        },
        {
          "line": 1795,
          "text": "                    \"entry_rank\":     top_entry_rank.get(sym) or leader_rank_all.get(sym),"
        },
        {
          "line": 1796,
          "text": "                    \"strategy\":       \"E1R_UPTREND_EXECUTION_V0_1\","
        },
        {
          "line": 1797,
          "text": "                    \"entry_mode\":     \"e1r_uptrend_execution_v0_1\","
        },
        {
          "line": 1798,
          "text": "                    \"primary_reason\": _etype,"
        }
      ]
    },
    {
      "path": "src/engine/backtest.py",
      "line": 1859,
      "terms": [
        "e1r_uptrend_execution_enabled"
      ],
      "context": [
        {
          "line": 1857,
          "text": "                # 旧模式：trade_action()==\"BUY\" + Strict TopN"
        },
        {
          "line": 1858,
          "text": "                if action == \"BUY\":"
        },
        {
          "line": 1859,
          "text": "                    if e1r_uptrend_execution_enabled:"
        },
        {
          "line": 1860,
          "text": "                        skip_reasons[\"e1r_legacy_buy_blocked\"] += 1"
        },
        {
          "line": 1861,
          "text": "                        continue"
        }
      ]
    },
    {
      "path": "src/engine/backtest.py",
      "line": 1979,
      "terms": [
        "ls60"
      ],
      "context": [
        {
          "line": 1977,
          "text": "                    state, mom, rs, close_t, ma50_v, ma50_sl,"
        },
        {
          "line": 1978,
          "text": "                    ls, th, market_score_default,"
        },
        {
          "line": 1979,
          "text": "                    ls60_exit_mode=ls60_exit_mode,"
        },
        {
          "line": 1980,
          "text": "                )"
        },
        {
          "line": 1981,
          "text": "                # 一致性检查："
        }
      ]
    },
    {
      "path": "src/engine/backtest.py",
      "line": 1991,
      "terms": [
        "ls60"
      ],
      "context": [
        {
          "line": 1989,
          "text": "                            f\"action_reason_mismatch: {sym} \""
        },
        {
          "line": 1990,
          "text": "                            f\"sig_action={action} reason_action={reason_action} \""
        },
        {
          "line": 1991,
          "text": "                            f\"ls60_exit_mode={ls60_exit_mode} \""
        },
        {
          "line": 1992,
          "text": "                            f\"ls={ls:.1f} state={state} price={close_t:.2f} ma50={ma50_v:.2f}\""
        },
        {
          "line": 1993,
          "text": "                        )"
        }
      ]
    },
    {
      "path": "src/engine/backtest.py",
      "line": 2009,
      "terms": [
        "ls60"
      ],
      "context": [
        {
          "line": 2007,
          "text": "                        and reason_info.get(\"primary_reason\") == \"leader_score_below_60\""
        },
        {
          "line": 2008,
          "text": "                        and sym in holdings"
        },
        {
          "line": 2009,
          "text": "                        and holdings[sym].get(\"ls60_reduce_triggered\")):"
        },
        {
          "line": 2010,
          "text": "                    skip_reasons[\"ls60_reduce_already_triggered\"] += 1"
        },
        {
          "line": 2011,
          "text": "                    continue"
        }
      ]
    },
    {
      "path": "src/engine/backtest.py",
      "line": 2010,
      "terms": [
        "ls60"
      ],
      "context": [
        {
          "line": 2008,
          "text": "                        and sym in holdings"
        },
        {
          "line": 2009,
          "text": "                        and holdings[sym].get(\"ls60_reduce_t
```

## Next Stage

- `Stage 3.8E-2F-2C-4C-10F-4B-0B`: Recover exact E1R core_variant_result source
- Recommended action: Use metric artifact candidates and e1r_composer/backtest source to recover the exact E1R frozen core_variant_result, then compare its daily equity/metrics against saved E1 5Y core.

