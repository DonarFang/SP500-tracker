# FD-M3180125 SA-step-2 Verification Contract v1.0 (FROZEN)

SA-step-2 consumes immutable SA-step-1 detections and produces verification evidence only.

## Required gates

1. The raw official document hash must match the SA-step-1 detection.
2. The announcement must contain a complete, reciprocal ADD/REMOVE pair for the S&P 500.
3. Publication and effective-date semantics must be deterministic and internally consistent.
4. Each official S&P symbol must resolve to exactly one Yahoo Finance symbol.
5. Equal symbols are permitted as the default only after Yahoo returns valid daily prices.
6. Non-equal symbols require an explicit, versioned mapping with evidence; punctuation substitution is never inferred.
7. Yahoo must return at least one finite, positive daily close for every candidate symbol.

Any missing, conflicting, ambiguous, or unavailable identity is `ENTRY_QUARANTINE`; the detection is `VERIFICATION_HOLD` and must include `manual_intervention_required=true` plus actionable failure codes.

## Frozen exclusions

SA-step-2 must not create Membership Events, publish Universe Snapshots or pointers, write prices, run Forward/Live/5Y, call a broker, or modify Engine strategy. Event creation belongs exclusively to SA-step-3.

## Allowed implementation paths

- `.github/workflows/sp500-source-verification-daily.yml`
- `config/sp500_source_automation/provider_symbol_map.json`
- `docs/contracts/FD-M3180125_SA_STEP_2_VERIFICATION_CONTRACT_v1.0_FROZEN_2026-08-22.md`
- `scripts/run_fd_m3180125_sp500_source_verification.py`
- `src/e1r_engine/source_automation/__init__.py`
- `src/e1r_engine/source_automation/verification.py`
- `tests/test_fd_m3180125_sa_step_2_source_verification.py`

Runtime evidence is restricted to `data/sp500_source_verification/**`.
