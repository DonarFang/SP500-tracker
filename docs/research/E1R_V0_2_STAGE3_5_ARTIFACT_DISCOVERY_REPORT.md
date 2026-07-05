# E1R v0.2 Stage 3.5 Artifact Discovery Report

Generated At: `2026-07-05T15:45:29.057461+00:00`

## Status

- Stage: `B_STAGE_3_5_ARTIFACT_DISCOVERY`
- Status: `DISCOVERED_E1R_V0_2_FROZEN_ARTIFACTS`
- Variant: `E1R_REGIME_AWARE_V0_2`

## Selected Sources

- Equity source file: `exports/e1r_candidates.json`
- Equity JSON path: `$.candidates`
- Equity rows: `8819`
- Summary source file: `exports/e1r_v0_2_backtest_summary.json`
- Summary JSON path: `$.v0_2`

## Method

- Recursively inspected feature `exports`, `data/research/e1_5y`, and `docs/research` JSON artifacts.
- Selected the highest-scoring E1R v0.2 equity series based on real date/equity-like rows.
- Selected the highest-scoring E1R v0.2 summary object based on real metric keys and E1R markers.

