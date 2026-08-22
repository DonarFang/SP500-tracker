#!/usr/bin/env python3
from __future__ import annotations
import argparse
from datetime import date
import json
from pathlib import Path
import subprocess
from typing import Any
from e1r_engine.live_calendar import load_live_trading_calendar
from e1r_engine.live_composition import (
    compose_active_live_production,
    discover_live_eligible_stock_symbols,
    discover_live_stock_symbols,
)

LIVE_ROOT=Path("exports/official/FD-M3180125-SP500-TOP3-engine/live")
PRICE_ROOT=Path("data/live_prices")
STATUS_PATH=LIVE_ROOT/"automation/current_data_update.json"
CALENDAR_PATH=Path("config/live_calendar/us_equity_calendar_v1.0.json")

def load_json(path: Path)->dict[str,Any]:
    payload=json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload,dict): raise RuntimeError(f"expected object: {path}")
    return payload

def _git_head()->str:
    return subprocess.check_output(["git","rev-parse","HEAD"],cwd=Path.cwd(),text=True).strip()

def main()->int:
    parser=argparse.ArgumentParser()
    parser.add_argument("--uv-shadow-probe",action="store_true")
    parser.add_argument("--uv-shadow-activation-time",default="2026-08-10T00:00:00Z")
    args=parser.parse_args()
    state=load_json(LIVE_ROOT/"runtime/current/runtime_state.json")
    if state.get("status")!="ACTIVE" or state.get("opening_activated") is not True or state.get("activation_required") is not False:
        raise RuntimeError("Personal Live runtime is not fully ACTIVE")
    status=load_json(STATUS_PATH)
    if status.get("data_status")!="CURRENT": raise RuntimeError("Live data status is not CURRENT")
    market_date=date.fromisoformat(str(status["latest_market_date"]))
    opening_date=date.fromisoformat(str(state["opening_date"]))
    if market_date<opening_date:
        print(json.dumps({"decision":"PASS_LIVE_ACTIVE_WAITING_FOR_OPENING_DATE_DATA","opening_date":opening_date.isoformat(),"latest_market_date":market_date.isoformat(),"opening_activated":True},indent=2,sort_keys=True)); return 0
    last_raw=state.get("last_committed_market_date")
    if not args.uv_shadow_probe and last_raw is not None and market_date<=date.fromisoformat(str(last_raw)):
        print(json.dumps({"decision":"PASS_LIVE_ACTIVE_NO_NEW_DATE","market_date":market_date.isoformat(),"last_committed_market_date":str(last_raw),"opening_activated":True},indent=2,sort_keys=True)); return 0
    live_calendar=load_live_trading_calendar(CALENDAR_PATH)
    expected_execution_date=live_calendar.next_session(market_date)
    if args.uv_shadow_probe:
        from e1r_engine.universe_versioning.shadow_integration import ShadowObserverConfig,UniverseShadowObserver
        catalogue=discover_live_stock_symbols(price_root=PRICE_ROOT,expected_stock_count=494)
        eligible,excluded=discover_live_eligible_stock_symbols(price_root=PRICE_ROOT,market_date=market_date,catalogue_stock_symbols=catalogue)
        account_path=LIVE_ROOT/"runtime/current/account_state.json"
        account=load_json(account_path) if account_path.is_file() else {"positions":state.get("positions",{})}
        positions=account.get("positions",{})
        if not isinstance(positions,dict): raise RuntimeError("HOLD_UV_STEP_3_LIVE_SHADOW: positions must be an object")
        recommendation_path=LIVE_ROOT/"runtime/current/latest_recommendations.json"
        recommendations=load_json(recommendation_path) if recommendation_path.is_file() else {}
        rows=recommendations.get("recommendations",recommendations.get("orders",[]))
        candidate_actions=rows if isinstance(rows,list) else []
        observer=UniverseShadowObserver(ShadowObserverConfig(repo_root=Path.cwd(),track="live",authority_head=_git_head(),activation_time=args.uv_shadow_activation_time))
        result=observer.observe(market_date=market_date.isoformat(),expected_execution_date=expected_execution_date.isoformat(),production_catalogue=catalogue,production_eligible=eligible,holdings_symbols=positions.keys(),data_ready_symbols=eligible,required_indices=("SPX","NDX","SOX","VIX"),candidate_actions=candidate_actions,date_source="LIVE_CALENDAR_HARD_GATE",protected_paths=(PRICE_ROOT,LIVE_ROOT))
        output=result.to_dict()
        output.update({"market_date":market_date.isoformat(),"production_catalogue_hash_source":"discover_live_stock_symbols","excluded_stock_symbols":list(excluded),"production_runs_performed":False,"production_data_updated":False,"production_membership_activated":False,"production_side_effect_calls":[]})
        print(json.dumps(output,ensure_ascii=False,indent=2,sort_keys=True)); return 0
    from e1r_engine.universe_versioning.production_integration import ProductionUniverseGate
    production_gate=ProductionUniverseGate(Path.cwd(),"live")
    universe_decision=None
    eligible_override=None
    required_override=None
    if production_gate.mode()=="ENFORCE":
        catalogue=discover_live_stock_symbols(price_root=PRICE_ROOT,expected_stock_count=494)
        eligible,_excluded=discover_live_eligible_stock_symbols(price_root=PRICE_ROOT,market_date=market_date,catalogue_stock_symbols=catalogue)
        account_path=LIVE_ROOT/"runtime/current/account_state.json"
        account=load_json(account_path) if account_path.is_file() else {"positions":state.get("positions",{})}
        positions=account.get("positions",{})
        if not isinstance(positions,dict): raise RuntimeError("HOLD_UV_STEP_4_LIVE_PRODUCTION: positions must be an object")
        universe_decision=production_gate.resolve(expected_execution_date=expected_execution_date.isoformat(),production_catalogue=catalogue,production_eligible=eligible,holdings_symbols=positions.keys(),data_ready_symbols=eligible,required_indices=("SPX","NDX","SOX","VIX"))
        eligible_override=universe_decision.eligible_buy_universe
        required_override=tuple(symbol for symbol in universe_decision.required_data_universe if symbol not in {"SPX","NDX","SOX","VIX"})
    composition=compose_active_live_production(price_root=PRICE_ROOT,live_root=LIVE_ROOT,data_status_path=STATUS_PATH,market_date=market_date,expected_execution_date=expected_execution_date,expected_stock_count=494,min_bars=120,eligible_stock_symbols_override=eligible_override,required_data_symbols_override=required_override)
    result=composition.runtime.dry_run(market_date=composition.market_date,market_data=composition.market_data)
    if universe_decision is not None:
        actions=tuple({"symbol":row.symbol,"action":row.action} for row in result.decision.position_recommendations)
        final_decision=production_gate.resolve(expected_execution_date=expected_execution_date.isoformat(),production_catalogue=composition.catalogue_stock_symbols,production_eligible=composition.required_data_symbols,holdings_symbols=result.account.positions.keys(),data_ready_symbols=composition.required_data_symbols,required_indices=("SPX","NDX","SOX","VIX"),candidate_actions=actions)
        if final_decision.blocked_risk_increases: raise RuntimeError("HOLD_UV_STEP_4_LIVE_PRODUCTION: Engine BUY/ADD failed pre-publication Universe gate")
    committed=composition.runtime.commit_active_daily(result=result,expected_execution_date=expected_execution_date)
    committed.update({"catalogue_stock_symbol_count":len(composition.catalogue_stock_symbols),"eligible_stock_symbol_count":len(composition.stock_symbols),"excluded_stock_symbols":list(composition.excluded_stock_symbols),"workflow_created":True,"broker_api_connected":False,"universe_production_mode":production_gate.mode(),"universe_evidence_hash":None if universe_decision is None else universe_decision.evidence_hash})
    print(json.dumps(committed,ensure_ascii=False,indent=2,sort_keys=True)); return 0

if __name__=="__main__": raise SystemExit(main())
