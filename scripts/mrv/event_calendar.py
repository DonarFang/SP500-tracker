"""Local official event calendars, 14-day review and November next-year preparation."""
import gzip,calendar,datetime as dt,hashlib,html,json,re,uuid
from pathlib import Path
from zoneinfo import ZoneInfo
UTC=dt.timezone.utc
NY=ZoneInfo('America/New_York')
PERIOD=dt.timedelta(days=14)
SEED='config/mrv/event-calendar-2026.json'
BASE='data/mrv/event-calendar'
def urls(year):return {'BLS':'https://www.bls.gov/schedule/%04d/home.htm'%year,'FED':'https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm'}
def active_path(year):return BASE+'/active.json' if year==2026 else BASE+'/years/%d/active.json'%year
def state_path(year):return BASE+'/review-state.json' if year==2026 else BASE+'/years/%d/review-state.json'%year
def stamp(s):
 d=dt.datetime.fromisoformat(s)
 if d.tzinfo is None:raise ValueError('CALENDAR_TIMEZONE_REQUIRED')
 return d

def validate(c,now,year=None):
 if c.get('schema')!='MRV_LOCAL_EVENTS_1' or c.get('timezone')!='America/New_York':raise ValueError('LOCAL_CALENDAR_SCHEMA')
 start=dt.date.fromisoformat(c['coverage_start']);end=dt.date.fromisoformat(c['coverage_end'])
 if year is None:year=start.year
 if year<2026 or start!=dt.date(year,1,1) or end!=dt.date(year,12,31):raise ValueError('LOCAL_CALENDAR_COVERAGE_CONTRACT')
 if stamp(c['verified_utc'])>now:raise ValueError('LOCAL_CALENDAR_FUTURE_VERIFICATION')
 if set(c['sources'])!=set(urls(year)):raise ValueError('LOCAL_CALENDAR_SOURCES')
 for k,s in c['sources'].items():
  if s['url']!=urls(year)[k] or not re.fullmatch('[0-9a-f]{64}',s['sha256']):raise ValueError('LOCAL_CALENDAR_SOURCE_IDENTITY')
  if stamp(s['retrieved_utc'])>stamp(c['verified_utc']):raise ValueError('LOCAL_CALENDAR_SOURCE_TIME')
 ev=c['events'];seen=set()
 if not isinstance(ev,list):raise ValueError('LOCAL_CALENDAR_EVENTS')
 for r in ev:
  day=dt.date.fromisoformat(r['date']);key=(r['date'],r['event'])
  if day.year!=year or r['event'] not in ['CPI','NFP','FOMC'] or key in seen:raise ValueError('LOCAL_CALENDAR_EVENT_INVALID')
  seen.add(key)
 if {r['event'] for r in ev}!={'CPI','NFP','FOMC'}:raise ValueError('LOCAL_CALENDAR_CATEGORY_MISSING')
 if ev!=sorted(ev,key=lambda r:(r['date'],r['event'])):raise ValueError('LOCAL_CALENDAR_ORDER')
 return c

def clean(s):return ' '.join(html.unescape(re.sub('<[^>]+>',' ',s)).split())
def parse(bls,fed,year):
 if '</html>' not in bls.lower() or '</html>' not in fed.lower():raise ValueError('REVIEW_INCOMPLETE_HTML')
 if 'All times on calendar are Eastern Time' not in clean(bls):raise ValueError('REVIEW_BLS_TIMEZONE')
 for name in calendar.month_name[1:]:
  if not re.search(r'<h[1-6][^>]*>\s*'+name+' '+str(year)+r'\s*</h[1-6]>',bls,re.I):raise ValueError('REVIEW_BLS_ANNUAL_COVERAGE:'+name)
 events=[]
 for tr in re.findall(r'<tr\b[^>]*>(.*?)</tr>',bls,re.S|re.I):
  s=clean(tr);kind='CPI' if 'Consumer Price Index for' in s else 'NFP' if 'Employment Situation for' in s else None
  if not kind:continue
  m=re.match(r'\w+, (\w+) (\d{1,2}), ('+str(year)+r') ',s)
  if not m or '08:30 AM' not in s:raise ValueError('REVIEW_BLS_ROW')
  events.append({'date':dt.date(year,list(calendar.month_name).index(m[1]),int(m[2])).isoformat(),'event':kind})
 m=re.search(r'<h4[^>]*>\s*(?:<a[^>]*>)?'+str(year)+r' FOMC Meetings(?:</a>)?\s*</h4>(.*?)(?=<h4|\Z)',fed,re.S)
 if not m:raise ValueError('REVIEW_FED_PANEL')
 pairs=re.findall(r'<div[^>]*class="[^"]*fomc-meeting__month[^"]*"[^>]*>(.*?)</div>\s*<div[^>]*class="[^"]*fomc-meeting__date[^"]*"[^>]*>(.*?)</div>',m[1],re.S)
 for month,days in pairs:
  month=clean(month);days=clean(days).replace('*','').strip()
  if not re.fullmatch(r'\d{1,2}-\d{1,2}',days):raise ValueError('REVIEW_FED_UNUSUAL_MEETING_MANUAL_REQUIRED')
  names=month.split('/');lookup={n:i for i,n in enumerate(calendar.month_name) if n};lookup.update({n:i for i,n in enumerate(calendar.month_abbr) if n})
  if not 1<=len(names)<=2 or any(n not in lookup for n in names):raise ValueError('REVIEW_FED_MONTH')
  if len(names)==2 and lookup[names[1]]!=lookup[names[0]]+1:raise ValueError('REVIEW_FED_MONTH_RANGE')
  startday,endday=map(int,days.split('-'))
  begin=dt.date(year,lookup[names[0]],startday);end=dt.date(year,lookup[names[-1]],endday)
  if (end-begin).days!=1:raise ValueError('REVIEW_FED_MEETING_RANGE')
  events.append({'date':end.isoformat(),'event':'FOMC'})
 return sorted(events,key=lambda r:(r['date'],r['event']))

def initial_coverage(c):
 # Conservative automatic bootstrap only. Atypical/cancelled releases require explicit review,
 # not invented dates. Later year revisions can have fewer releases.
 for kind in ['CPI','NFP']:
  if {dt.date.fromisoformat(r['date']).month for r in c['events'] if r['event']==kind}!=set(range(1,13)):raise ValueError('NEW_YEAR_INCOMPLETE_OR_ATYPICAL_'+kind)
 if sum(r['event']=='FOMC' for r in c['events'])!=8:raise ValueError('NEW_YEAR_FOMC_SCHEDULE_MANUAL_REVIEW')

def read_active(root,safe,now,year):
 p=safe(root,active_path(year))
 if not p.exists() and year==2026:p=safe(root,SEED)
 if not p.exists():return None
 return validate(json.loads(p.read_bytes()),now,year)

def compatibility(root,year,now,safe,write):
 """Engineering checks only: frozen artifacts and synthetic cross-year inputs, not OOS validation."""
 import run as m
 import math
 calpath=safe(root,'config/live_calendar/us_equity_calendar_v1.0.json')
 cal=m.live_calendar.load_live_trading_calendar(calpath);b=m.bundle(root)
 fingerprint=m.digest(m.encoded({'year':year,'bundle':b['bundle_id'],'calendar':m.digest(calpath.read_bytes()),'run':m.digest((root/'scripts/mrv/run.py').read_bytes()),'adapter':m.digest(Path(__file__).read_bytes())}))
 report=safe(root,BASE+'/years/%d/compatibility.json'%year)
 if report.exists():
  old=json.loads(report.read_bytes())
  if old.get('fingerprint')==fingerprint and old.get('status')=='PASS':return old
 result={'year':year,'fingerprint':fingerprint,'checked_utc':now.isoformat(),'status':'FAIL','evidence_class':'ENGINEERING_SYNTHETIC_NOT_PREDICTIVE_PERFORMANCE'}
 try:
  if dt.date(year,1,1)<cal.coverage_start or dt.date(year,12,31)>cal.coverage_end:raise ValueError('TRADING_CALENDAR_YEAR_NOT_COVERED')
  first=dt.date(year,1,1)
  while not cal.is_session(first):first+=dt.timedelta(days=1)
  prior=first-dt.timedelta(days=1)
  while not cal.is_session(prior):prior-=dt.timedelta(days=1)
  if prior.year!=year-1 or cal.next_session(prior)!=first:raise ValueError('YEAR_BOUNDARY_SESSION')
  golden=m.selftest(root)
  if b['probability_error']:raise ValueError('PROBABILITY_ARTIFACT_NOT_VERIFIED')
  dates=m.prior_sessions(cal,prior);spx={};vix={};terms={'VIX9D':{},'VIX3M':{}}
  for i,d in enumerate(dates):
   price=100+i*.1+math.sin(i*.4)
   spx[d]={'open':price-.1,'high':price+1,'low':price-1,'close':price};vix[d]=20+math.sin(i*.3)
   terms['VIX9D'][d]=vix[d]*.95;terms['VIX3M'][d]=vix[d]*1.05
  f,used=m.features(cal,prior,first,spx,vix,terms)
  if len(used)!=70 or used[-1]!=prior.isoformat() or any(d>=first.isoformat() for d in used):raise ValueError('CROSS_YEAR_FEATURE_WINDOW')
  ordinary=m.infer(b,f,[]);event=m.infer(b,f,['CPI'])
  if ordinary['probabilities'] is None or event['probabilities'] is None or event['final_grade']!='severe':raise ValueError('CROSS_YEAR_INFERENCE')
  spx[first.isoformat()]={'open':1,'high':99999,'low':.001,'close':99999};vix[first.isoformat()]=999
  f2,_=m.features(cal,prior,first,spx,vix,terms)
  if any(f[k]!=f2[k] for k in m.REQUIRED):raise ValueError('TARGET_DATA_LEAKAGE')
  result.update(status='PASS',signal_date=prior.isoformat(),target_date=first.isoformat(),history_days=len(used),golden=golden,checks=['calendar_year_coverage','year_boundary','frozen_artifacts','70_session_window','no_target_price_input','probability_output','event_override'])
 except Exception as ex:result['error']=str(ex)
 write(report,result)
 if result['status']!='PASS':raise ValueError('CROSS_YEAR_COMPATIBILITY:'+result['error'])
 return result

def review(root,out,now,fetch,safe,write,year,force=False,files=None):
 c=read_active(root,safe,now,year);statefile=safe(root,state_path(year))
 state=json.loads(statefile.read_bytes()) if statefile.exists() else {}
 last=stamp(state['attempted_utc']) if state.get('attempted_utc') else stamp(c['verified_utc']) if c else None
 if last and last>now:raise ValueError('CALENDAR_REVIEW_STATE_FUTURE')
 if not force and last and now<last+PERIOD:return c,state
 result={'year':year,'attempted_utc':now.isoformat(),'next_attempt_utc':(now+PERIOD).isoformat(),'status':'FAILED','error':None}
 folder=safe(root,BASE+'/reviews/%d-'%year+now.strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:6]);folder.mkdir(parents=True)
 try:
  blobs={};sources={}
  for name,url in urls(year).items():
   if files:
    blobs[name]=Path(files[name]).read_bytes();sources[name]={'url':url,'sha256':hashlib.sha256(blobs[name]).hexdigest(),'retrieved_utc':now.isoformat(),'mode':'USER_SUPPLIED_OFFICIAL_HTML'}
   else:blobs[name],sources[name]=fetch(url,folder,name)
   (folder/(name+'.gz')).write_bytes(gzip.compress(blobs[name],mtime=0))
  checked=max(now,dt.datetime.now(UTC))
  candidate={'schema':'MRV_LOCAL_EVENTS_1','timezone':'America/New_York','coverage_start':'%d-01-01'%year,'coverage_end':'%d-12-31'%year,'events':parse(blobs['BLS'].decode('utf-8-sig'),blobs['FED'].decode('utf-8-sig'),year),'sources':sources,'verified_utc':checked.isoformat()}
  validate(candidate,checked,year)
  before={(r['date'],r['event']) for r in c['events']} if c else set();after={(r['date'],r['event']) for r in candidate['events']}
  delta={'removed':sorted(before-after),'added':sorted(after-before)}
  write(folder/'candidate.json',candidate);write(folder/'changes.json',delta)
  result.update(candidate=str((folder/'candidate.json').relative_to(root)),changes=delta)
  if c is None:
   initial_coverage(candidate);result['compatibility']=compatibility(root,year,now,safe,write)
   write(safe(root,active_path(year)),candidate);c=candidate;result['status']='NEW_YEAR_READY'
  elif before==after:
   if year>2026:result['compatibility']=compatibility(root,year,now,safe,write)
   write(safe(root,active_path(year)),candidate);c=candidate;result['status']='VERIFIED_UNCHANGED'
  else:result['status']='CHANGES_PENDING_APPROVAL'
 except Exception as e:result['error']=type(e).__name__+':'+str(e)
 write(folder/'result.json',result);write(statefile,result)
 return c,result

def prepare(root,out,now,fetch,safe,write):
 local=now.astimezone(NY);years=[local.year]
 if local.month>=11:years.append(local.year+1)
 statuses={}
 for year in years:
  try:
   c,s=review(root,out,now,fetch,safe,write,year)
   if c is not None and year>2026:compatibility(root,year,now,safe,write)
   statuses[str(year)]={'year':year,'available':c is not None,'review_status':s.get('status','NOT_DUE'),'last_attempt_utc':s.get('attempted_utc'),'next_attempt_utc':s.get('next_attempt_utc'),'error':s.get('error'),'pending_changes':s.get('status')=='CHANGES_PENDING_APPROVAL'}
  except Exception as ex:statuses[str(year)]={'year':year,'available':False,'review_status':'FAILED','error':str(ex)}
 payload={'checked_utc':now.isoformat(),'current_year':local.year,'next_year':local.year+1,'preparation_enabled':local.month>=11,'years':statuses,'rule':'NOVEMBER_START_14_DAY_INTERVAL','trading_calendar_note':'Shared trading calendar is frozen; insufficient year coverage blocks activation.'}
 write(out/'annual-calendar-status.json',payload);write(safe(root,'exports/mrv/calendar-preparation.json'),payload)
 return payload

def load(root,out,now,target,fetch,safe,write):
 preparation=prepare(root,out,now,fetch,safe,write)
 c=read_active(root,safe,max(now,dt.datetime.now(UTC)),target.year)
 if c is None:raise ValueError('LOCAL_CALENDAR_YEAR_NOT_READY:'+str(target.year))
 if not c['coverage_start']<=target.isoformat()<=c['coverage_end']:raise ValueError('LOCAL_CALENDAR_TARGET_OUTSIDE_COVERAGE')
 if target.year>2026:compatibility(root,target.year,now,safe,write)
 statefile=safe(root,state_path(target.year));state=json.loads(statefile.read_bytes()) if statefile.exists() else {}
 overdue=now>=stamp(c['verified_utc'])+PERIOD
 health={'LOCAL':{'calendar_mode':'LOCAL_VERIFIED','year':target.year,'verified_utc':c['verified_utc'],'review_due_utc':(stamp(c['verified_utc'])+PERIOD).isoformat(),'coverage_start':c['coverage_start'],'coverage_end':c['coverage_end'],'review_overdue':overdue,'review_status':state.get('status','NOT_DUE'),'last_attempt_utc':state.get('attempted_utc'),'review_error':state.get('error'),'pending_changes':state.get('status')=='CHANGES_PENDING_APPROVAL'},'ANNUAL_PREPARATION':preparation}
 write(out/'event-calendar-used.json',c)
 return c['events'],health,c['sources']

def main():
 import argparse
 import run
 ap=argparse.ArgumentParser(description='Official local calendar review, no model retraining. Commit/push separately.')
 ap.add_argument('--year',type=int);ap.add_argument('--force',action='store_true');ap.add_argument('--bls-file',type=Path);ap.add_argument('--fed-file',type=Path);ap.add_argument('--approve',type=Path)
 a=ap.parse_args();now=dt.datetime.now(UTC);root=run.ROOT;year=a.year or now.astimezone(NY).year
 out=root/BASE;out.mkdir(parents=True,exist_ok=True)
 if a.approve:
  c=validate(json.loads(a.approve.read_bytes()),now,a.year);year=dt.date.fromisoformat(c['coverage_start']).year
  if now-stamp(c['verified_utc'])>=PERIOD:raise ValueError('APPROVAL_CANDIDATE_TOO_OLD')
  if year>2026:compatibility(root,year,now,run.safe,run.write)
  old=read_active(root,run.safe,now,year)
  archive=out/'approvals'/(now.strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:6]+'.json')
  run.write(archive,{'old':old,'new':c,'approved_utc':now.isoformat(),'candidate':str(a.approve)})
  run.write(run.safe(root,active_path(year)),c);run.write(run.safe(root,state_path(year)),{'year':year,'attempted_utc':now.isoformat(),'next_attempt_utc':(now+PERIOD).isoformat(),'status':'MANUALLY_APPROVED'})
  print('CALENDAR_APPROVAL=PASS; commit/push data/mrv/event-calendar, then run MRV Daily Observation.');return
 if bool(a.bls_file)!=bool(a.fed_file):ap.error('Supply both official HTML files')
 c,s=review(root,out,now,run.fetch,run.safe,run.write,year,force=a.force or bool(a.bls_file),files={'BLS':a.bls_file,'FED':a.fed_file} if a.bls_file else None)
 print(json.dumps(s,ensure_ascii=False,indent=2))
 if s.get('status')=='FAILED':raise SystemExit(1)
if __name__=='__main__':main()
