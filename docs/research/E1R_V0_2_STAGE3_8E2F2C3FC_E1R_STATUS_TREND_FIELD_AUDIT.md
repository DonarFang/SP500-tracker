# Stage 3.8E-2F-2C-3F-C E1R Status Trend Field Audit

Generated At: `2026-07-08T09:55:01.750357+00:00`

## Status

- Status: `AUDIT_COMPLETE_NO_SOURCE_CHANGES`
- Dashboard changed: `False`
- Exports changed: `False`
- State changed: `False`
- Workflow changed: `False`

## Files

- script_exists: `True`
- status_export_exists: `True`
- market_state_exists: `True`

## Status Export Candidates

- top_level_trend_candidate: `regime = UPTREND`
- top_level_subclass_candidate: `subclass = None`
- top_level_state_candidate: `None = None`
- nested_candidates_count: `2`

## Script JSON Path References

- `data/research/e1_5y/raw/indices/SPX.json`
- `data/research/e1_5y/regimes/spx_regime_daily.json`
- `exports/e1r_v0_2_status.json`
- `exports/market_state.json`

## Script Output/Regime Lines

- L34: `def normalize_e1r_state(regime: str, subclass: str) -> str:`
- L35: `    r = (regime or "UNKNOWN").upper()`
- L36: `    s = (subclass or "").upper()`
- L53: `def extract_latest_regime(regime_json: Any) -> dict[str, Any]:`
- L54: `    daily = regime_json.get("daily_regime") if isinstance(regime_json, dict) else regime_json`
- L59: `            raise RuntimeError("daily_regime list is empty")`
- L66: `            raise RuntimeError("daily_regime dict is empty")`
- L75: `    raise RuntimeError("Unsupported spx_regime_daily.json structure")`
- L78: `def extract_legacy_market_state(path: Path) -> dict[str, Any]:`
- L87: `        "state": pick(market, ["state", "market_state", "trend_state", "regime"], None),`
- L106: `    regime_path = ROOT / "data/research/e1_5y/regimes/spx_regime_daily.json"`
- L109: `    legacy_market_path = ROOT / "exports/market_state.json"`
- L112: `    regime_json = read_json(regime_path)`
- L113: `    latest = extract_latest_regime(regime_json)`
- L116: `    regime = str(pick(latest, ["regime", "market_regime", "state"], "UNKNOWN")).upper()`
- L117: `    subclass = str(pick(latest, ["subclass", "regime_subclass", "market_subclass", "sideways_subclass"], "") or "").upper()`
- L118: `    e1r_market_state = normalize_e1r_state(regime, subclass)`
- L123: `        allowed_subclasses=("MA_CONFLICT",),`
- L135: `        regime_path=regime_path,`
- L160: `    sidecar_active = e1r_market_state == "SIDEWAYS_MA_CONFLICT" and len(holdings) > 0`
- L161: `    core_active = e1r_market_state == "UPTREND"`
- L169: `        "e1r_market_state": e1r_market_state,`
- L170: `        "regime": regime,`
- L171: `        "subclass": subclass or None,`
- L189: `        "legacy_market_state": extract_legacy_market_state(legacy_market_path),`
- L191: `            "regime": str(regime_path.relative_to(ROOT)),`
- L194: `            "legacy_market_state": str(legacy_market_path.relative_to(ROOT)),`
- L208: `    print("e1r_market_state:", status["e1r_market_state"])`
- L209: `    print("regime:", status["regime"])`
- L210: `    print("subclass:", status["subclass"])`

## Diagnosis

- exports/e1r_v0_2_status.json top-level trend candidate found: regime=UPTREND
- scripts/export_e1r_v0_2_status.py contains regime/trend-related output lines.
- Script references 4 JSON path(s); inspect path_refs for input source.

## Open Questions

- Does e1r_v0_2_status.json already expose the global trend state directly?
- If the status export exposes trend_state, is it generated from the same market-regime logic we want globally?
- If not, which upstream JSON or function supplies UPTREND/SIDEWAYS/DOWNTREND?

