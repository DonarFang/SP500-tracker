"""
validation.py — Data Validation Layer  [Rev.2 Section 4]
"""
from __future__ import annotations
from datetime import datetime, timedelta
from ..utils.config import EXPORTS_DIR
from ..utils.helpers import read_json, write_json, price_file
from ..utils import logger

MIN_UNIVERSE = 500
MIN_BARS     = 450

def validate_universe(symbols):
    ok = len(symbols)>=MIN_UNIVERSE
    return {"check":"universe","count":len(symbols),"min":MIN_UNIVERSE,
            "status":"PASS" if ok else "FAIL",
            "message":f"成分股 {len(symbols)} 只{'✅' if ok else f' ❌ 不足{MIN_UNIVERSE}只'}"}

def validate_history(symbols):
    valid=0; failed=[]; incomplete=[]
    for s in symbols:
        rec=read_json(price_file(s))
        if not rec: failed.append(s); continue
        n=len(rec)
        if n>=MIN_BARS: valid+=1
        else: incomplete.append({"symbol":s,"bars":n})
    cov=round(valid/len(symbols)*100,1) if symbols else 0
    st="PASS" if cov>=80 else "WARN" if cov>=60 else "FAIL"
    return {"check":"history","valid_symbols":valid,"failed_symbols":len(failed),
            "incomplete":len(incomplete),"total":len(symbols),"coverage_pct":cov,
            "status":st,"message":f"覆盖率 {cov}% ({valid}/{len(symbols)} 只达标 ≥{MIN_BARS}bars)"}

def validate_freshness(symbols):
    import pytz; ET=pytz.timezone("America/New_York")
    now=datetime.now(ET); cutoff=(now-timedelta(days=3)).strftime("%Y-%m-%d")
    dates=[]
    for s in symbols[:50]:
        rec=read_json(price_file(s))
        if rec: dates.append(rec[-1].get("date",""))
    if not dates: return {"check":"freshness","status":"FAIL","message":"无价格数据","latest_date":""}
    latest=max(dates); st="PASS" if latest>=cutoff else "WARN"
    return {"check":"freshness","latest_date":latest,"status":st,"message":f"最新日期：{latest}"}

def run_validation(symbols) -> dict:
    try:
        import pytz; ET=pytz.timezone("America/New_York")
    except:
        from datetime import timezone, timedelta; ET=timezone(timedelta(hours=-4))
    now=datetime.now(ET)
    logger.info("  [Validation] 数据质量检查...")
    vu=validate_universe(symbols); vh=validate_history(symbols); vf=validate_freshness(symbols)
    checks=[vu,vh,vf]
    overall="FAIL" if any(c["status"]=="FAIL" for c in checks) else "WARN" if any(c["status"]=="WARN" for c in checks) else "PASS"
    health={"generated_at":now.isoformat(),
            "generated_at_display":now.strftime("%Y年%-m月%-d日 %H:%M ET"),
            "data_status":overall,"universe_count":vu["count"],
            "valid_symbols":vh["valid_symbols"],"failed_symbols":vh["failed_symbols"],
            "history_coverage_pct":vh["coverage_pct"],
            "latest_data_date":vf.get("latest_date",""),
            "signal_engine_enabled":overall!="FAIL",
            "checks":{"universe":vu,"history":vh,"freshness":vf}}
    icon="✅" if overall=="PASS" else "⚠️" if overall=="WARN" else "❌"
    logger.info(f"  [Validation] {icon} {overall}: {vu['message']} | {vh['message']}")
    EXPORTS_DIR.mkdir(parents=True,exist_ok=True)
    write_json(EXPORTS_DIR/"data_health.json", health)
    logger.ok("data_health.json 已生成")
    return health
