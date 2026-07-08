# Stage 3.8E-2F-2C-3F-B Trend Regime Source Audit

Generated At: `2026-07-08T09:51:47.452371+00:00`

## Status

- Status: `AUDIT_COMPLETE_NO_SOURCE_CHANGES`
- Dashboard changed: `False`
- Exports changed: `False`
- State changed: `False`
- Workflow changed: `False`

## Diagnosis

- Found 79 candidate files containing trend/regime terms.
- Top candidate: docs/research/E1R_V0_2_IMPLEMENTATION_MANIFEST.md with terms DETERIORATION_TRANSITION, DOWNTREND, MA_CONFLICT, RECOVERY_TRANSITION, SIDEWAYS, UPTREND, regime, subclass.
- exports/market_state.json does not currently expose trend_state/market_regime/regime.

## Top Candidate Source Files

- `docs/research/E1R_V0_2_IMPLEMENTATION_MANIFEST.md` score `17` terms `DETERIORATION_TRANSITION, DOWNTREND, MA_CONFLICT, RECOVERY_TRANSITION, SIDEWAYS, UPTREND, regime, subclass`
  - L17: `SIDEWAYS:MA_CONFLICT Top10 25% daily rebalanced sidecar sleeve`
  - L21: `- UPTREND: use unchanged E1R_REGIME_AWARE_V0_1 logic.`
  - L22: `- SIDEWAYS: sidecar sleeve may be active only when subclass is MA_CONFLICT.`
  - L23: `- SIDEWAYS:DETERIORATION_TRANSITION: no sidecar exposure.`
- `scripts/export_e1r_v0_2_status.py` score `15` terms `DOWNTREND, MA_CONFLICT, SIDEWAYS, UPTREND, market_regime, market_state, regime, sideways_subclass, subclass, trend_state`
  - L34: `def normalize_e1r_state(regime: str, subclass: str) -> str:`
  - L35: `    r = (regime or "UNKNOWN").upper()`
  - L36: `    s = (subclass or "").upper()`
  - L39: `        return "UPTREND"`
- `docs/research/E1R_V0_2_OOS_SUMMARY_FIELD_AUDIT.json` score `13` terms `DOWNTREND, MA_CONFLICT, SIDEWAYS, UPTREND, market_state, regime, subclass`
  - L49: `          "market_state",`
  - L50: `          "regime",`
  - L51: `          "subclass",`
  - L69: `        "regime": true,`
- `docs/research/E1R_V0_2_STAGE3_8E2F1A_FORWARD_SOURCE_AUDIT.json` score `13` terms `DOWNTREND, MA_CONFLICT, SIDEWAYS, UPTREND, market_regime, market_state, regime, sideways_subclass, subclass, trend_state`
  - L285: `          "text": "        ms = json.loads((exports / \"market_state.json\").read_text())"`
  - L350: `          "text": "        ms = json.loads((exports / \"market_state.json\").read_text())"`
  - L360: `          "text": "        logger.error(f\"Cannot load market_state.json: {e}\")"`
  - L375: `          "text": "        market_state=mkt_state,"`
- `docs/research/E1R_V0_2_STAGE3_8E2F1E0_TARGET_ACTION_INPUT_AUDIT.json` score `13` terms `DOWNTREND, MA_CONFLICT, SIDEWAYS, UPTREND, market_state, regime, subclass`
  - L41: `    "exports/market_state.json",`
  - L200: `        "SIDEWAYS": [`
  - L203: `        "MA_CONFLICT": [`
  - L679: `          "term": "SIDEWAYS",`
- `docs/research/E1R_V0_2_STAGE3_8E2F1E0_TARGET_ACTION_INPUT_AUDIT.md` score `13` terms `DOWNTREND, MA_CONFLICT, SIDEWAYS, UPTREND, market_state, regime, subclass`
  - L35: `- `exports/market_state.json``
  - L40: `- `scripts/run_e1r_v0_2_oos.py` lines=`180` defs=`['read_json', 'write_json', 'main']` hit_terms=`['target', 'target_weight', 'weight', 'selected', 'selected_count', 'symbols', 'top', 'top_n', 'core', 'sidecar', 'sleeve', 'gross_exposure', 'position', 'positions', 'order', 'order`
  - L43: `- `scripts/export_e1r_v0_2_status.py` lines=`217` defs=`['read_json', 'write_json', 'pick', 'normalize_e1r_state', 'extract_latest_regime', 'extract_legacy_market_state', 'simplify_holding', 'main']` hit_terms=`['weight', 'selected', 'selected_count', 'symbols', 'top', 'top_n', '`
  - L45: `- `src/engine/e1r_composer.py` lines=`360` defs=`['safe_float', 'pct_display', 'compound_return', 'max_drawdown', 'sharpe_ratio', 'profit_factor', 'extract_core_interval_returns', 'build_equity_records_from_returns', 'summarize_combined_variant', 'compose_e1r_v0_2_variant']` hit_`
- `docs/research/E1R_V0_2_STAGE3_8E2F1E1_TARGET_SOURCE_CONTRACT.json` score `13` terms `DOWNTREND, MA_CONFLICT, SIDEWAYS, UPTREND, market_state, regime, subclass, trend_state`
  - L37: `        "market_state/regime/subclass",`
  - L80: `        "preview": "{\n  \"active\": false,\n  \"active_condition\": \"SIDEWAYS_MA_CONFLICT\",\n  \"gross_exposure\": 0.25,\n  \"top_n\": 10,\n  \"excluded_symbols\": [\n    \"VIXY\"\n  ],\n  \"selected_count\": 0,\n  \"selected\": [],\n  \"source_record_date\": \"2026-06-17\",\n`
  - L90: `          "regime",`
  - L91: `          "subclass",`
- `docs/research/E1R_V0_2_STAGE3_8E2F1F0_DAILY_PIPELINE_AUDIT.json` score `13` terms `DOWNTREND, MA_CONFLICT, SIDEWAYS, UPTREND, market_regime, market_state, regime, sideways_subclass, subclass, trend_state`
  - L125: `      "preview": "   1: #!/usr/bin/env python3\n   2: \"\"\"\n   3: run_oos.py — Forward/OOS Tracking Engine entry point v1.1\n   4: Usage:\n   5:   python3 run_oos.py                        # run for today (NO_OP on weekends/holidays)\n   6:   python3 run_oos.py --date 2026-06-1`
  - L252: `      "preview": "   1: from __future__ import annotations\n   2: \n   3: import json\n   4: import runpy\n   5: from datetime import datetime, timezone\n   6: from pathlib import Path\n   7: from typing import Any\n   8: \n   9: ROOT = Path(__file__).resolve().parents[1]\n  10: `
  - L395: `          "text": "    legacy_market_path = ROOT / \"exports/market_state.json\"",`
  - L408: `      "preview": "   1: from __future__ import annotations\n   2: \n   3: import json\n   4: import sys\n   5: from datetime import datetime, timezone\n   6: from pathlib import Path\n   7: from typing import Any\n   8: \n   9: ROOT = Path(__file__).resolve().parents[1]\n  10: sy`

## Workflow Hits

- L29: `          python run_oos.py --check`
- L35: `        run: python run_oos.py`
- L41: `          python3 scripts/export_e1r_v0_2_status.py`
- L42: `          python3 scripts/run_e1r_v0_2_oos.py`
- L43: `          python3 scripts/run_e1r_v0_2_oos_equity.py`
- L44: `          python3 scripts/export_e1r_v0_2_targets_preview.py`
- L45: `          python3 scripts/export_e1r_v0_2_orders_positions_preview.py`
- L46: `          python3 scripts/run_e1r_v0_2_forward_performance.py`

## Next Patch Should

- Patch the true market_state export generator if it already has access to trend regime.
- If trend regime is only available from E1R export, first decide whether it is acceptable to source global Market card from E1R export.
- Avoid hardcoding UPTREND in dashboard.
- Dashboard should display Trend State and Risk Mode separately only after trend_state source is explicit.

