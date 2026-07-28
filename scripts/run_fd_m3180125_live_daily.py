#!/usr/bin/env python3
from __future__ import annotations
from datetime import date, timedelta
import json
from pathlib import Path
from typing import Any
from e1r_engine.live_composition import compose_active_live_production

LIVE_ROOT=Path("exports/official/FD-M3180125-SP500-TOP3-engine/live")
PRICE_ROOT=Path("data/live_prices")
STATUS_PATH=LIVE_ROOT/"automation/current_data_update.json"

def load_json(path: Path)->dict[str,Any]:
    payload=json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload,dict): raise RuntimeError(f"expected object: {path}")
    return payload

def next_weekday(day: date)->date:
    candidate=day+timedelta(days=1)
    while candidate.weekday()>=5: candidate+=timedelta(days=1)
    return candidate

def main()->int:
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
    if last_raw is not None and market_date<=date.fromisoformat(str(last_raw)):
        print(json.dumps({"decision":"PASS_LIVE_ACTIVE_NO_NEW_DATE","market_date":market_date.isoformat(),"last_committed_market_date":str(last_raw),"opening_activated":True},indent=2,sort_keys=True)); return 0
    expected_execution_date=next_weekday(market_date)
    composition=compose_active_live_production(price_root=PRICE_ROOT,live_root=LIVE_ROOT,data_status_path=STATUS_PATH,market_date=market_date,expected_execution_date=expected_execution_date,expected_stock_count=494,min_bars=120)
    result=composition.runtime.dry_run(market_date=composition.market_date,market_data=composition.market_data)
    committed=composition.runtime.commit_active_daily(result=result,expected_execution_date=expected_execution_date)
    committed.update({"catalogue_stock_symbol_count":len(composition.catalogue_stock_symbols),"eligible_stock_symbol_count":len(composition.stock_symbols),"excluded_stock_symbols":list(composition.excluded_stock_symbols),"workflow_created":True,"broker_api_connected":False})
    print(json.dumps(committed,ensure_ascii=False,indent=2,sort_keys=True)); return 0

if __name__=="__main__": raise SystemExit(main())
