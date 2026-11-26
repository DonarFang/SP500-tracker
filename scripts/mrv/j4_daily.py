"""Run frozen J4 without executing legacy LINEAR4. Standard library; no training at runtime."""
import argparse,datetime as dt,hashlib,json,sys,traceback,uuid,zipfile,shutil
from pathlib import Path
import run as io
import event_calendar as ec
import j4_model as model
ROOT=io.ROOT;UTC=io.UTC;BASE='exports/mrv/j4';MODEL='J4_joint';CLASSES=('light','moderate','severe')
def window(t,target,events):
    return sorted({(r['date'],r['event'],'发布日' if r['date']==str(target) else '发布后首个交易日') for r in events if str(t)<=r['date']<=str(target)})
def rows(cal,t,spx,vix):
    ds=io.prior_sessions(cal,t,26)
    return ds,[[spx[d]['high'],spx[d]['low'],spx[d]['close'],vix[d]] for d in ds]
def selftest(root):
    b=model.bundle(root);fixtures=io.read(root/'config/mrv/J4-golden.json')
    if len(fixtures)<40:raise ValueError('GOLDEN_INCOMPLETE')
    for date,ww,n,s,g in fixtures:
        a,h,c=model.infer(b,model.features(ww,b))
        if max(abs(a-n),abs(h-s))>1e-12 or c!=g:raise ValueError('J4_PARITY:'+date)
    for low,expected in [(98.8,'light'),(98.799,'moderate'),(97.5,'moderate'),(97.499,'severe')]:
        if model.label(100,low)[1]!=expected:raise ValueError('J4_BOUNDARY')
    if window('2026-04-02','2026-04-06',[{'date':'2026-04-03','event':'NFP'}])!=[('2026-04-03','NFP','发布后首个交易日')]:raise ValueError('J4_HOLIDAY')
    return {'model':MODEL,'golden':len(fixtures),'status':'PASS'}
def check_year(root,cal,year):
    first=dt.date(year,1,1)
    if first<cal.coverage_start or dt.date(year,12,31)>cal.coverage_end:raise ValueError('TRADING_CALENDAR_YEAR_NOT_COVERED')
    while not cal.is_session(first):first+=dt.timedelta(days=1)
    t=first-dt.timedelta(days=1)
    while not cal.is_session(t):t-=dt.timedelta(days=1)
    ds=io.prior_sessions(cal,t,26)
    if cal.next_session(t)!=first or len(set(ds))!=26 or max(ds)!=str(t) or t.year!=year-1:raise ValueError('J4_YEAR_BOUNDARY')
    if len(window(t,first,[{'date':str(t),'event':'CPI'},{'date':str(first),'event':'NFP'}]))!=2:raise ValueError('J4_YEAR_EVENTS')
    return dict(selftest(root),year=year,feature_date=str(t),target_date=str(first),evidence_class='ENGINEERING_ONLY')
def run(root,out,now):
    cal=io.live_calendar.load_live_trading_calendar(root/'config/live_calendar/us_equity_calendar_v1.0.json')
    b=model.bundle(root);t=io.latest_completed(cal,now);target=cal.next_session(t)
    raw=out/'raw';raw.mkdir();ev,health,provenance=ec.load(root,out,now,target,io.fetch,io.safe,io.write)
    if t.year!=target.year:
        prev=ec.read_active(root,io.safe,max(now,dt.datetime.now(UTC)),t.year)
        if not prev:raise ValueError('PREVIOUS_YEAR_EVENT_CALENDAR_MISSING')
        ev=prev['events']+ev;io.write(out/'prior-year-calendar-used.json',prev)
    evs=window(t,target,ev)
    sources={};sp,sources['SPX']=io.fetch('https://query1.finance.yahoo.com/v8/finance/chart/%5EGSPC?range=1y&interval=1d&includePrePost=false',raw,'SPX')
    vx,sources['VIX']=io.fetch('https://cdn.cboe.com/api/global/us_indices/daily_prices/VIX_History.csv',raw,'VIX')
    spx=io.yahoo(sp,'^GSPC');vix=io.cboe(vx);ds,w=rows(cal,t,spx,vix)
    n,s,g=model.infer(b,model.features(w,b));final='severe' if evs else g
    now2=dt.datetime.now(UTC);opened=io.moment(target,9,30);base=io.safe(root,BASE)
    facts=dict(model=MODEL,bundle_id=model.HASH,feature_date=str(t),target_date=str(target),previous_close=w[-1][2],source_sessions=ds,input_hash=io.digest(io.encoded(w)),events=evs,score_nonmild=n,score_severe=s,model_grade=g,final_grade=final,thresholds=b['cut'],probabilities=None,probability_status='NOT_CALIBRATED')
    pid=io.digest(io.encoded(facts))
    p=dict(facts,prediction_id=pid,generated_utc=now2.isoformat(),evidence_class='BEFORE_TARGET_OPEN' if now2<opened else 'LATE_RECONSTRUCTION',target_close_utc=io.moment(target,13 if target in cal.early_close_sessions else 16).astimezone(UTC).isoformat(),data_ready_utc=io.moment(target,18).astimezone(UTC).isoformat(),calendar_health=health,sources=sources,event_calendar_sha256=io.digest(io.encoded(ev)))
    first=base/'predictions'/(str(target)+'.json');rev=False
    if first.exists():
        old=io.read(first)
        if old['prediction_id']==pid:p=old
        else:
            rev=True;p['revision_of']=old['prediction_id'];rp=base/'revisions'/str(target)/(pid+'.json')
            if rp.exists():p=io.read(rp)
            else:io.write(rp,p,True)
    else:io.write(first,p,True)
    history=[]
    for path in sorted((base/'predictions').glob('*.json')):
        orig=io.read(path);d=orig['target_date'];ap=base/'actuals'/(d+'.json')
        if not ap.exists() and now>=io.moment(dt.date.fromisoformat(d),18) and d in spx:
            loss,grade=model.label(orig['previous_close'],spx[d]['low'])
            io.write(ap,dict(date=d,loss=loss,**{'class':grade},target_low=spx[d]['low'],previous_close=orig['previous_close'],prediction_id=orig['prediction_id'],model=MODEL,source=sources['SPX'],recorded_utc=now2.isoformat()),True)
        history.append(dict({k:orig[k] for k in ['model','target_date','model_grade','final_grade','evidence_class','events','prediction_id']},actual=io.read(ap) if ap.exists() else None))
    io.write(out/'input-window.json',dict(sessions=ds,columns=['high','low','close','vix'],rows=w))
    dest=io.safe(root,'data/mrv/j4-snapshots/'+pid);dest.mkdir(parents=True,exist_ok=True)
    for src in [*raw.iterdir(),out/'event-calendar-used.json',out/'prior-year-calendar-used.json',out/'input-window.json']:
        if src.exists() and not (dest/src.name).exists():shutil.copyfile(src,dest/src.name)
    io.write(base/'history.json',history);io.write(base/'latest.json',dict(p,is_revision=rev))
    status=dict(status='READY',model=MODEL,target_date=str(target),feature_date=str(t),prediction_id=pid,checked_utc=now2.isoformat(),calendar_health=health)
    io.write(base/'status.json',status);io.write(out/'prediction.json',p);io.write(out/'result.json',status)
    print('J4_DAILY=READY TARGET='+str(target))
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--self-test',action='store_true');ap.add_argument('--report-root',type=Path,default=Path.home()/'UEIS-MRV/reports/step4');a=ap.parse_args()
    if a.self_test: print(json.dumps(selftest(ROOT)));return
    now=dt.datetime.now(UTC);out=a.report_root/('MRV-J4-'+now.strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:6]);out.mkdir(parents=True)
    try:run(ROOT,out,now)
    except Exception as ex:
        status=dict(status='BLOCKED',model=MODEL,checked_utc=dt.datetime.now(UTC).isoformat(),error=str(ex))
        io.write(out/'result.json',status);io.write(ROOT/BASE/'status.json',status);raise
    finally:
        io.write(out/'manifest.json',{str(p.relative_to(out)):io.digest(p.read_bytes()) for p in out.rglob('*') if p.is_file()})
if __name__=='__main__':main()
