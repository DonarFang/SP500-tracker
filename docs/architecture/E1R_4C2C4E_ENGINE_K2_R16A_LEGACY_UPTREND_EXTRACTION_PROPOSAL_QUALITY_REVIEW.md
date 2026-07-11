# E1R K2 R16A Legacy UPTREND Extraction Proposal Quality Review

Generated UTC: 2026-07-11T09:52:40.546918+00:00

Decision: PASS_WITH_ARTIFACT_COMPACTION_REQUIRED

## Scope

R16A is a quality review only.

No legacy strategy file, standalone engine file, account logic, market gate logic, or execution logic was modified.

## Artifact size

- research_json: 29755 lines, 977153 bytes
- research_md: 411 lines, 40320 bytes
- architecture_md: 411 lines, 40320 bytes
- audit_json: 29755 lines, 977153 bytes
- evidence_json: 18 lines, 655 bytes

- Total: 60350 lines, 2035601 bytes

## Duplicate analysis

- research JSON equals audit JSON: True
- research Markdown equals architecture Markdown: True

## Category quality

- candidate_generation: legacy_hits=60, standalone_hits=31, classification=MIXED_LEGACY_AND_STANDALONE
- ranking_and_top3_selection: legacy_hits=86, standalone_hits=18, classification=MIXED_LEGACY_AND_STANDALONE
- buy_generation: legacy_hits=59, standalone_hits=16, classification=MIXED_LEGACY_AND_STANDALONE
- add_generation: legacy_hits=42, standalone_hits=11, classification=MIXED_LEGACY_AND_STANDALONE
- hold_behavior: legacy_hits=68, standalone_hits=9, classification=MIXED_LEGACY_AND_STANDALONE
- reduce_behavior: legacy_hits=77, standalone_hits=9, classification=MIXED_LEGACY_AND_STANDALONE
- exit_behavior: legacy_hits=89, standalone_hits=21, classification=MIXED_LEGACY_AND_STANDALONE
- position_sizing: legacy_hits=6, standalone_hits=3, classification=MIXED_LEGACY_AND_STANDALONE
- pending_order_boundary: legacy_hits=17, standalone_hits=0, classification=LEGACY_ONLY
- next_day_execution: legacy_hits=32, standalone_hits=0, classification=LEGACY_ONLY
- market_gate_consumption: legacy_hits=60, standalone_hits=56, classification=MIXED_LEGACY_AND_STANDALONE
- account_mutation: legacy_hits=25, standalone_hits=43, classification=MIXED_LEGACY_AND_STANDALONE
- uptrend_branch: legacy_hits=60, standalone_hits=42, classification=MIXED_LEGACY_AND_STANDALONE

## Main legacy evidence functions

- src/engine/backtest.py:run_stateful_simulation: 411 hits
- src/engine/backtest.py:MODULE: 52 hits
- src/engine/backtest.py:run_action_forward_validation: 48 hits
- src/engine/trade_decision.py:trade_action_reason: 44 hits
- src/engine/trade_decision.py:trade_action: 35 hits
- src/engine/backtest.py:run_trade_rule_validation: 16 hits
- src/engine/backtest.py:run_promotion_engine_validation: 14 hits
- src/engine/trade_decision.py:MODULE: 13 hits
- src/engine/backtest.py:_e1r_risk_budget_for_regime: 11 hits
- src/engine/backtest.py:_e1r_mode_for_regime: 6 hits
- src/engine/backtest.py:_load_e1r_regime_daily: 5 hits
- src/engine/backtest.py:_rebuild_leader_score: 4 hits

## Quality findings

- R16 research JSON and audit JSON are byte-for-byte duplicates.
- R16 research Markdown and architecture Markdown are byte-for-byte duplicates.
- R16 artifacts exceed the compact-review threshold.
- Standalone engine hits are mixed into the legacy evidence index.

## Recommended actions

- Compact R16 artifacts before or together with the next evidence stage.
- Keep one canonical detailed JSON and one compact human-review Markdown.
- Replace duplicated audit and architecture payloads with summaries and references.
- Use legacy-only function and variable traces for R17; do not treat standalone R14/R15 code as legacy proof.

## Next stage

R16B_ARTIFACT_COMPACTION_AND_LEGACY_ONLY_EVIDENCE_INDEX
