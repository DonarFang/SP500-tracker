#!/usr/bin/env python3
"""Frozen LINEAR4 daily observation; Python >=3.9, standard library only."""
import argparse,bisect,calendar,csv,datetime as dt,gzip,hashlib,html,io,json,math,os,re,sys,time,traceback,types,urllib.request,uuid
from pathlib import Path
from zoneinfo import ZoneInfo
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'vendor'))
import core,daily,engine,incremental,combo,calibrate,live_calendar
import calendar_sources
NY=ZoneInfo('America/New_York'); UTC=dt.timezone.utc
VERSION='MRV-step-4-v1.1'; ROOT=HERE.parents[1]
REQUIRED=['term3m','vix','spx_downside20','term9','spx_dd60','spx_rv5','spx_tail_max5','spx_range','spx_dd20','spx_down20','spx_ma20_gap','spx_down10','vix_delta5','rv5_20']

def digest(b):return hashlib.sha256(b).hexdigest()
def encoded(obj):return (json.dumps(obj,ensure_ascii=False,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
def read(p):return json.loads(p.read_bytes())
def safe(root,rel):
 p=root/rel
 if Path(rel).is_absolute() or '..' in Path(rel).parts:raise ValueError('UNSAFE_PATH')
 q=p
 while q!=root:
  if q.is_symlink():raise ValueError('SYMLINK:'+str(q))
  q=q.parent
 return p

def write(p,obj,immutable=False):
 p.parent.mkdir(parents=True,exist_ok=True);blob=encoded(obj)
 if immutable:
  if p.exists():
   if p.read_bytes()!=blob:raise ValueError('IMMUTABLE_CONFLICT:'+str(p))
   return
  with p.open('xb') as f:f.write(blob)
 else:
  tmp=p.with_name(p.name+'.tmp-'+uuid.uuid4().hex);tmp.write_bytes(blob);os.replace(tmp,p)

def bundle(root):
 cfg=root/'config/mrv';manifest=read(cfg/'manifest.json');prob_error=None
 for rel,h in manifest.items():
  p=safe(root,rel)
  if not p.is_file() or digest(p.read_bytes())!=h:
   if rel.endswith('/P2_BETA.json'):prob_error='PROBABILITY_ARTIFACT_MISSING_OR_CHANGED';continue
   raise ValueError('FROZEN_HASH_MISMATCH:'+rel)
 out={n:read(cfg/(n+'.json')) for n in ['ALL12_M7','LONG10_M6','I7R','I6V','LINEAR4','stress-cdf']}
 out['P2_BETA']=None if prob_error else read(cfg/'P2_BETA.json');out['probability_error']=prob_error
 out['bundle_id']=digest((cfg/'manifest.json').read_bytes());return out

def infer(b,f,events):
 if any(k not in f or f[k] is None or not math.isfinite(f[k]) for k in REQUIRED):raise ValueError('REQUIRED_FEATURE_MISSING')
 four={};solver=types.SimpleNamespace(sigmoid=incremental.sigmoid)
 for key,name in [('F7','ALL12_M7'),('F6','LONG10_M6')]:
  m=b[name]['model'];four[key]=engine.predict(m,[[f[k] for k in m['features']]],solver,None)[0]
 dist=b['stress-cdf'];value=f['spx_downside20'];q=(bisect.bisect_left(dist,value)+bisect.bisect_right(dist,value))/2/len(dist);stress=max(0,2*q-1)
 extra={'stress_vix_cooling':stress*max(0,-f['vix_delta5']),'stress_rv_cooling':stress*max(0,-f['rv5_20']),'vix_delta5':f['vix_delta5']}
 for name,key in [('I7R','F7'),('I6V','F6')]:
  a=b[name];x=incremental.raw_input(a['base'],four[key],extra,incremental.SPECS[name][1]);four[name]=incremental.predict(incremental.transform([x],a['scaler']),a['model'])[0]
 score=combo.score(b['LINEAR4'],four);threshold=b['LINEAR4']['threshold']
 grade='severe' if score>threshold else 'light' if four['F7']<=b['ALL12_M7']['thresholds']['moderate'] else 'moderate'
 final='severe' if events else grade
 pp=None;prob_error=b['probability_error']
 if b['P2_BETA'] is not None:
  try:
   p=calibrate.predict(b['P2_BETA'],{'score':score,'events':events,'final_grade':final});calibrate.check(p)
   if any(v is None for v in p):raise ValueError('PROBABILITY_PARTIAL')
   pp=dict(zip(['light','moderate','severe','moderate_or_severe'],p))
  except Exception as e:prob_error=str(e)
 return {'four_scores':four,'score':score,'severe_threshold':threshold,'model_grade':grade,'final_grade':final,'events':events,'probabilities':pp,'probability_error':prob_error,'probability_status':'OBSERVATION_ESTIMATE' if pp else 'UNAVAILABLE','probability_model':'P2_BETA_FINAL','model':'LINEAR4_T2021_2022','bundle_id':b['bundle_id']}

def clean(s):return ' '.join(html.unescape(re.sub('<[^>]+>',' ',s)).split())
def parse_events(bls,fed,year):
 ev=[]
 if bls.lstrip().startswith('BEGIN:VCALENDAR'):
  ev=calendar_sources.ics_events(bls.lstrip(),year)
 else:
  for tr in re.findall(r'<tr\b[^>]*>(.*?)</tr>',bls,re.S|re.I):
   s=clean(tr);kind='CPI' if 'Consumer Price Index for' in s else 'NFP' if 'Employment Situation for' in s else None
   if not kind:continue
   m=re.match(r'\w+, (\w+) (\d{1,2}), (\d{4}) ',s)
   if not m:raise ValueError('BLS_SCHEMA_CHANGED:'+s[:100])
   date=dt.date(int(m[3]),list(calendar.month_name).index(m[1]),int(m[2])).isoformat()
   if int(m[3])!=year:raise ValueError('BLS_YEAR_MISMATCH')
   ev.append({'date':date,'event':kind})
 # Bound parsing to a single annual panel; minutes and press releases are not events.
 m=re.search(r'<h4[^>]*>\s*(?:<a[^>]*>)?'+str(year)+r' FOMC Meetings(?:</a>)?\s*</h4>(.*?)(?=<h4|\Z)',fed,re.S)
 if not m:raise ValueError('FED_YEAR_PANEL_MISSING')
 pairs=re.findall(r'<div[^>]*class="[^"]*fomc-meeting__month[^"]*"[^>]*>(.*?)</div>\s*<div[^>]*class="[^"]*fomc-meeting__date[^"]*"[^>]*>(.*?)</div>',m[1],re.S)
 for month,days in pairs:
  month=clean(month);days=clean(days).replace('*','').strip()
  if not re.fullmatch(r'\d{1,2}-\d{1,2}',days):raise ValueError('FED_UNREVIEWED_MEETING:'+days)
  if month not in list(calendar.month_name):raise ValueError('FED_UNREVIEWED_MONTH:'+month)
  date=dt.date(year,list(calendar.month_name).index(month),int(days.split('-')[-1])).isoformat();ev.append({'date':date,'event':'FOMC'})
 counts={k:sum(r['event']==k for r in ev) for k in ['CPI','NFP','FOMC']}
 if counts!={'CPI':12,'NFP':12,'FOMC':8} or len({(r['date'],r['event']) for r in ev})!=32:raise ValueError('EVENT_COVERAGE_REQUIRES_REVIEW:'+str(counts))
 return sorted(ev,key=lambda r:(r['date'],r['event']))

def fetch(url,out,name):
 errors=[]
 for attempt in range(3):
  try:
   req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 MRV-observation/1.0','Accept':'*/*'})
   with urllib.request.urlopen(req,timeout=40) as response:blob=response.read(30*1024*1024+1)
   if not blob or len(blob)>30*1024*1024:raise ValueError('EMPTY_OR_OVERSIZED_SOURCE')
   (out/(name+'.gz')).write_bytes(gzip.compress(blob,mtime=0))
   return blob,{'url':url,'sha256':digest(blob),'retrieved_utc':dt.datetime.now(UTC).isoformat(),'raw':name+'.gz'}
  except Exception as e:
   errors.append(type(e).__name__+':'+str(e))
   if isinstance(e,urllib.error.HTTPError) and e.code in [401,403,404]:break
   time.sleep(min(2*attempt,4))
 raise ValueError('SOURCE_UNAVAILABLE:'+name+':'+str(errors))

def yahoo(blob,symbol):
 j=json.loads(blob);chart=j['chart']
 if chart.get('error') or len(chart.get('result') or [])!=1:raise ValueError('YAHOO_RESPONSE:'+symbol)
 r=chart['result'][0]
 zone={'^GSPC':'America/New_York','^VIX':'America/Chicago'}[symbol]
 if r['meta'].get('symbol')!=symbol or r['meta'].get('exchangeTimezoneName')!=zone:raise ValueError('YAHOO_IDENTITY:'+symbol)
 if r['meta'].get('dataGranularity')!='1d':raise ValueError('YAHOO_INTERVAL')
 q=r['indicators']['quote'][0];out={}
 for i,t in enumerate(r['timestamp']):
  day=dt.datetime.fromtimestamp(t,ZoneInfo(zone)).date().isoformat();v={k:q[k][i] for k in ['open','high','low','close']}
  if any(x is None for x in v.values()):continue
  if day in out or any(not math.isfinite(x) or x<=0 for x in v.values()) or not v['low']<=min(v['open'],v['close'])<=max(v['open'],v['close'])<=v['high']:raise ValueError('YAHOO_OHLC_INVALID:'+day)
  out[day]=v
 return out

def cboe(blob):
 rr=csv.DictReader(io.StringIO(blob.decode('utf-8-sig')));out={}
 if not {'DATE','CLOSE'}<=set(rr.fieldnames or []):raise ValueError('CBOE_SCHEMA')
 for r in rr:
  day=dt.datetime.strptime(r['DATE'],'%m/%d/%Y').date().isoformat();x=float(r['CLOSE'])
  if day in out or not math.isfinite(x) or x<=0:raise ValueError('CBOE_VALUE')
  out[day]=x
 return out

def moment(day,hour,minute=0):return dt.datetime.combine(day,dt.time(hour,minute),NY)
def latest_completed(cal,now):
 day=now.astimezone(NY).date()
 for _ in range(15):
  if cal.is_session(day) and now>=moment(day,18):return day
  day-=dt.timedelta(days=1)
 raise ValueError('LATEST_SESSION_UNRESOLVED')
def prior_sessions(cal,t,n=70):
 out=[];d=t
 while len(out)<n:
  if cal.is_session(d):out.append(d.isoformat())
  d-=dt.timedelta(days=1)
 return list(reversed(out))

def features(cal,t,target,spx,vix,terms):
 ds=prior_sessions(cal,t)
 for day in ds:
  if day not in spx or day not in vix:raise ValueError('INCOMPLETE_SPX_VIX:'+day)
 for sym in ['VIX9D','VIX3M']:
  if t.isoformat() not in terms[sym]:raise ValueError('INCOMPLETE_TERM:'+sym+':'+t.isoformat())
 # Target is a date marker only; no target prices enter make_features.
 built=daily.make_features(ds+[target.isoformat()],{'SPX':{k:spx[k] for k in ds},'NDX':{}},{'VIX_CLOSE':{k:vix[k] for k in ds},'VVIX_VVIX':{}},{'SPX':set(),'NDX':set()},dict(terms,SKEW={}),core)
 return built[70],ds

def save_prediction(root,p):
 base=safe(root,'exports/mrv');target=p['target_date'];first=base/'predictions'/ (target+'.json')
 # Content fingerprint excludes fetch timestamp and raw paths. Same signal is idempotent.
 value={k:p[k] for k in ['target_date','feature_date','features','score','four_scores','model_grade','final_grade','events','probabilities','bundle_id']}
 p['prediction_id']=digest(encoded(value))
 if first.exists():
  old=read(first)
  if old['prediction_id']==p['prediction_id']:return old,False
  rev=base/'revisions'/target/(p['prediction_id']+'.json')
  if rev.exists():return read(rev),True
  p['revision_of']=old['prediction_id'];write(rev,p,True);return p,True
 write(first,p,True);return p,False

def run(root,out,now):
 cfg=safe(root,'config/live_calendar/us_equity_calendar_v1.0.json');cal=live_calendar.load_live_trading_calendar(cfg)
 b=bundle(root);t=latest_completed(cal,now);target=cal.next_session(t)
 if target.year!=2026:raise ValueError('FROZEN_ANNUAL_MODELS_ONLY_2026_REVIEW_REQUIRED')
 raw=out/'raw';raw.mkdir();sources={};inputs={}
 urls={'SPX':'https://query1.finance.yahoo.com/v8/finance/chart/%5EGSPC?range=1y&interval=1d&includePrePost=false','VIX':'https://query1.finance.yahoo.com/v8/finance/chart/%5EVIX?range=1y&interval=1d&includePrePost=false','VIX9D':'https://cdn-api.cboe.com/api/global/us_indices/daily_prices/VIX9D_History.csv','VIX3M':'https://cdn-api.cboe.com/api/global/us_indices/daily_prices/VIX3M_History.csv','BLS':'https://www.bls.gov/schedule/2026/home.htm','FED':'https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm'}
 for name,url in urls.items():
  print('FETCH='+name,flush=True)
  if name in ['BLS','FED']:
   inputs[name],sources[name]=calendar_sources.obtain(name,root,raw,fetch,dt.datetime.now(UTC),moment(target,9,30),safe)
  else:inputs[name],sources[name]=fetch(url,raw,name)
  write(out/'sources.json',sources)
 spx=yahoo(inputs['SPX'],'^GSPC');vix={k:v['close'] for k,v in yahoo(inputs['VIX'],'^VIX').items()};terms={k:cboe(inputs[k]) for k in ['VIX9D','VIX3M']}
 ev=parse_events(inputs['BLS'].decode('utf-8-sig'),inputs['FED'].decode('utf-8-sig'),2026)
 write(out/'events.json',ev)
 for name in ['BLS','FED']:calendar_sources.retain(name,inputs[name],sources[name],root,safe,write)
 calendar_health={name:{k:v for k,v in sources[name].items() if k in ['url','retrieved_utc','calendar_mode','cache_expires_utc']} for name in ['BLS','FED']}
 f,ds=features(cal,t,target,spx,vix,terms);events=[r['event'] for r in ev if r['date']==target.isoformat()]
 p=infer(b,f,events);created=dt.datetime.now(UTC)
 p.update(calendar_health=calendar_health,feature_date=t.isoformat(),target_date=target.isoformat(),generated_utc=created.isoformat(),target_open_utc=moment(target,9,30).astimezone(UTC).isoformat(),target_close_utc=moment(target,13 if target in cal.early_close_sessions else 16).astimezone(UTC).isoformat(),data_ready_utc=moment(target,18).astimezone(UTC).isoformat(),features={k:f[k] for k in REQUIRED},previous_close=spx[t.isoformat()]['close'],sources=sources,source_sessions=ds,event_calendar_sha256=digest(encoded(ev)),evidence_class='BEFORE_TARGET_OPEN' if created<moment(target,9,30) else 'LATE_RECONSTRUCTION',information_cutoff='T_CLOSE_NO_PREMARKET',source_quality='YAHOO_UNADJUSTED_EOD_PROXY_CBOE_EOD_NOT_EXCHANGE_TICK_CERTIFIED',version=VERSION)
 p,revision=save_prediction(root,p)
 base=safe(root,'exports/mrv');history=[]
 for path in sorted((base/'predictions').glob('*.json')):
  original=read(path);date=dt.date.fromisoformat(original['target_date']);actual_path=base/'actuals'/(date.isoformat()+'.json')
  if now>=moment(date,18) and date.isoformat() in spx and not actual_path.exists():
   loss,grade=daily.label(original['previous_close'],spx[date.isoformat()]['low'])
   write(actual_path,{'date':date.isoformat(),'loss':loss,'class':grade,'target_low':spx[date.isoformat()]['low'],'previous_close':original['previous_close'],'recorded_utc':created.isoformat(),'prediction_id':original['prediction_id'],'source':sources['SPX']},True)
  history.append({k:original[k] for k in ['target_date','feature_date','final_grade','model_grade','probabilities','generated_utc','evidence_class']})
  history[-1]['actual']=read(actual_path) if actual_path.exists() else None
 write(base/'history.json',history)
 write(base/'latest.json',dict(p,is_revision=revision,calendar_health=calendar_health));write(base/'status.json',{'status':'READY','calendar_health':calendar_health,'checked_utc':created.isoformat(),'feature_date':t.isoformat(),'target_date':target.isoformat(),'prediction_id':p['prediction_id'],'probability_status':p['probability_status']})
 # Preserve fetched snapshots once for each novel prediction; public source data only.
 dest=safe(root,'data/mrv/snapshots/'+p['prediction_id']);dest.mkdir(parents=True,exist_ok=True)
 for file in raw.iterdir():
  dst=dest/file.name
  if not dst.exists():dst.write_bytes(file.read_bytes())
 if not (dest/'sources.json').exists():write(dest/'sources.json',sources,True)
 write(out/'prediction.json',p);write(out/'result.json',{'status':'PASS','target_date':target.isoformat(),'evidence_class':p['evidence_class'],'revision':revision,'step5_acceptance':'PENDING_USER_RUN_REVIEW'})
 print('MRV_DAILY=PASS TARGET='+target.isoformat(),flush=True)

def selftest(root):
 b=bundle(root);g=read(root/'config/mrv/golden.json');fs={r['date']:r for r in g['features-2026.csv']};four={r['date']:r for r in g['four-scores-2026.csv']};count=0;maximum=0
 for r in g['predictions.csv']:
  if r['model']!='LINEAR4_T2021_2022':continue
  f={k:float(fs[r['date']][k]) for k in REQUIRED};p=infer(b,f,json.loads(r['events']))
  for k in four[r['date']]:
   if k in p['four_scores']:
    error=abs(p['four_scores'][k]-float(four[r['date']][k]));maximum=max(maximum,error)
    if error>1e-12:raise ValueError('GOLDEN_FOUR:'+r['date']+':'+k)
  if abs(p['score']-float(r['score']))>1e-12 or p['model_grade']!=r['model_grade'] or p['final_grade']!=r['final_grade']:raise ValueError('GOLDEN_GRADE:'+r['date'])
  count+=1
 if count!=199:raise ValueError('GOLDEN_COHORT')
 cal=live_calendar.load_live_trading_calendar(root/'config/live_calendar/us_equity_calendar_v1.0.json')
 for a,z in [('2026-10-30','2026-11-02'),('2026-11-25','2026-11-27'),('2026-11-27','2026-11-30'),('2026-12-24','2026-12-28')]:
  if cal.next_session(dt.date.fromisoformat(a)).isoformat()!=z:raise ValueError('CALENDAR_GOLDEN')
 assert daily.label(100,97)[1]=='severe' and daily.label(100,98.8)[1]=='light'
 try:infer(b,{},[])
 except ValueError:pass
 else:raise ValueError('MISSING_FEATURE_NOT_BLOCKED')
 return {'status':'PASS','historical_days':count,'four_score_max_error':maximum,'probability_artifact_status':b['probability_error'] or 'VERIFIED','calendar_cases':4}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--self-test',action='store_true');ap.add_argument('--report-root',type=Path,default=Path.home()/'UEIS-MRV/reports/step4');a=ap.parse_args()
 if a.self_test:print(json.dumps(selftest(ROOT)));return
 out=a.report_root.expanduser()/('MRV-step-4-Daily-'+dt.datetime.now(UTC).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:6]);out.mkdir(parents=True)
 failed=False;print('OUTPUT='+str(out),flush=True)
 try:run(ROOT,out,dt.datetime.now(UTC))
 except Exception as e:
  failed=True;traceback.print_exc();status={'status':'BLOCKED','checked_utc':dt.datetime.now(UTC).isoformat(),'error':str(e)};write(out/'result.json',status)
  write(safe(ROOT,'exports/mrv/status.json'),status)
 finally:
  import zipfile
  write(out/'manifest.json',{str(p.relative_to(out)):digest(p.read_bytes()) for p in out.rglob('*') if p.is_file()})
  with zipfile.ZipFile(out/'evidence.zip','w',zipfile.ZIP_DEFLATED) as z:
   for p in out.rglob('*'):
    if p.is_file() and p.name!='evidence.zip':z.write(p,str(p.relative_to(out)))
  print('EVIDENCE='+str(out/'evidence.zip'),flush=True)
 if failed:sys.exit(1)
if __name__=='__main__':main()
