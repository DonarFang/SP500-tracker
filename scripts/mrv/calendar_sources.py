"""Public official calendar adapters and bounded, transparent outage cache."""
import base64,datetime as dt,gzip,hashlib,json,re
from pathlib import Path
UTC=dt.timezone.utc
MAX_AGE=dt.timedelta(hours=72)
URLS={'BLS':['https://www.bls.gov/schedule/news_release/bls.ics','https://www.bls.gov/schedule/2026/home.htm'],'FED':['https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm']}
SEED_SHA='c9469114e223fcb47774fdc17a2b3caf6e3a20a213156e4b9994c4ee612e21d8'
def sha(b):return hashlib.sha256(b).hexdigest()
def ics_events(text,year):
 text=re.sub(r'\r?\n[ \t]','',text);out=[]
 if not text.startswith('BEGIN:VCALENDAR') or 'END:VCALENDAR' not in text:raise ValueError('BLS_ICS_ENVELOPE')
 for block in re.findall(r'BEGIN:VEVENT\s*(.*?)END:VEVENT',text,re.S):
  fields={}
  for line in block.splitlines():
   if ':' not in line:continue
   key,value=line.strip().split(':',1);key=key.split(';')[0]
   if key in fields:raise ValueError('ICS_DUPLICATE_FIELD:'+key)
   fields[key]=value
  kind={'Consumer Price Index':'CPI','Employment Situation':'NFP'}.get(fields.get('SUMMARY'))
  if not kind:continue
  start=re.search(r'^DTSTART;TZID=(?:US-Eastern|America/New_York):(\d{8})T083000\s*$',block,re.M)
  if not start or any(k in fields for k in ['RRULE','RECURRENCE-ID']):raise ValueError('ICS_EVENT_TIME_OR_RECURRENCE')
  day=dt.datetime.strptime(start[1],'%Y%m%d').date()
  if day.year!=year:continue
  if fields.get('STATUS')=='CANCELLED':raise ValueError('ICS_CANCELLED_EVENT_REVIEW')
  out.append({'date':day.isoformat(),'event':kind})
 if {k:sum(x['event']==k for x in out) for k in ['CPI','NFP']}!={'CPI':12,'NFP':12} or len({(r['date'],r['event']) for r in out})!=24:raise ValueError('ICS_FULL_YEAR_COVERAGE_REQUIRED')
 return out

def record(blob,meta):
 return {'raw_gzip_base64':base64.b64encode(gzip.compress(blob,mtime=0)).decode(),'source':{k:meta[k] for k in ['url','sha256','retrieved_utc']}}
def unpack(rec,name,now,target_open):
 source=rec['source'];stamp=dt.datetime.fromisoformat(source['retrieved_utc'])
 if stamp.tzinfo is None or stamp>now or now-stamp>MAX_AGE or target_open>stamp+MAX_AGE:raise ValueError('CALENDAR_CACHE_EXPIRED_OR_FUTURE:'+name)
 if source['url'] not in URLS[name]:raise ValueError('CALENDAR_CACHE_SOURCE:'+name)
 blob=gzip.decompress(base64.b64decode(rec['raw_gzip_base64'],validate=True))
 if sha(blob)!=source['sha256']:raise ValueError('CALENDAR_CACHE_HASH:'+name)
 return blob,dict(source,calendar_mode='CACHED',cache_expires_utc=(stamp+MAX_AGE).isoformat())

def obtain(name,root,out,fetch,now,target_open,safe):
 errors=[]
 for i,url in enumerate(URLS[name]):
  try:
   blob,meta=fetch(url,out,name if i==0 else name+'_ICS')
   return blob,dict(meta,calendar_mode='FRESH',fallback_attempts=errors)
  except ValueError as e:errors.append(str(e))
 records=[]
 cache=safe(root,'data/mrv/calendar-cache/'+name+'.json')
 if cache.exists():
  try:records.append(json.loads(cache.read_bytes()))
  except Exception as e:errors.append('CACHE_READ:'+str(e))
 seed=safe(root,'config/mrv/calendar-seed.json').read_bytes()
 if sha(seed)!=SEED_SHA:raise ValueError('CALENDAR_SEED_HASH')
 records.append(json.loads(seed)[name])
 for rec in sorted(records,key=lambda x:x.get('source',{}).get('retrieved_utc',''),reverse=True):
  try:
   blob,meta=unpack(rec,name,now,target_open)
   filename=name+'_CACHED.gz';(out/filename).write_bytes(gzip.compress(blob,mtime=0))
   return blob,dict(meta,raw=filename,fallback_attempts=errors)
  except Exception as e:errors.append(str(e))
 raise ValueError('CALENDAR_UNAVAILABLE:'+name+':'+str(errors))

def retain(name,blob,meta,root,safe,write):
 # Called only after full combined calendar validation; reuse never renews age.
 if meta['calendar_mode']=='FRESH':write(safe(root,'data/mrv/calendar-cache/'+name+'.json'),record(blob,meta))
