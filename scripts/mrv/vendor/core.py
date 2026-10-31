"""MRV 2A v2: bounded factor research, Python 3.9+, standard library only."""
import argparse,base64,bisect,csv,datetime as dt,fcntl,gzip,hashlib,io,json,math,os,platform,random,statistics as st,sys,tempfile,time,traceback,zipfile
from pathlib import Path,PurePosixPath
VERSION='MRV-step-2A-v2.0'
SEVERE=0.055969989661825176
MODERATE=0.026554930513974506
BASE=['vix','vix_delta5','rv5_20','rv20_60']
REGISTRY=[
 ('vix','baseline','log(VIX)'),('vix_delta5','baseline','log(VIX_t/VIX_t-5)'),
 ('rv5_20','baseline','log(RV5/RV20)'),('rv20_60','baseline','log(RV20/RV60)'),
 ('vix_d1','vol_speed','log(VIX_t/VIX_t-1)'),('vix_d3','vol_speed','log(VIX_t/VIX_t-3)'),
 ('vix_shock','vol_speed','(d1-mean(previous60 d1))/sd(previous60 d1)'),
 ('vix_accel','vol_speed','latest3-session log change minus preceding3-session log change'),
 ('vix_rise_run','vol_speed','consecutive positive daily VIX changes, capped at 5'),
 ('vvix_d1','vol_of_vol','log(VVIX_t/VVIX_t-1)'),('vvix_shock','vol_of_vol','VVIX d1 standardized by preceding60 daily log changes'),
 ('spx_down_z1','price_speed','negative latest SPX log return / preceding60 daily return sd'),
 ('spx_down_z3','price_speed','negative 3-session log return / (preceding60 return sd * sqrt(3))'),
 ('spx_down_accel','price_speed','negative latest3 minus preceding3 log return, divided by preceding60 sd * sqrt(3)'),
 ('spx_down_run','price_speed','consecutive negative SPX daily returns, capped at 5'),
 ('spx_range_burst','price_path','latest (high-low)/previous_close divided by mean of preceding20 such ranges'),
 ('spx_close_weak','price_path','(high-close)/(high-low); zero range is missing'),
 ('spx_gap_down','price_path','negative latest observed log(open/previous_close); NOT next opening gap'),
 ('ndx_weak3','cross_index','3-session SPX log return minus NDX log return'),
 ('term9','option_term','log(VIX9D/VIX); observations from 2014 onward only'),
 ('term9_d3','option_term','3-session change of log(VIX9D/VIX)'),
 ('term3m','option_term','log(VIX/VIX3M); observations from 2008 onward only'),
 ('term3m_d3','option_term','3-session change of log(VIX/VIX3M)'),
 ('skew','option_skew','SKEW level; observations from 2012 onward only; NOT physical crash probability'),
 ('skew_d5','option_skew','SKEW 5-session change')]
PENDING=[
 ('weekly_put_tail','option_tail','BLOCKED_OPTION_CHAIN','7-14 day put skew/tail; historical chains and availability needed'),
 ('effective_spread','liquidity','BLOCKED_INTRADAY_QUOTES','constituent-weighted effective spread; historical universe and trades needed'),
 ('amihud','liquidity','BLOCKED_DOLLAR_VOLUME','abs(return)/dollar volume; index OHLC volume is not a substitute'),
 ('hy_oas_d5','credit','BLOCKED_PIT_AND_HISTORY','HY OAS 5-session widening; reference data cannot be promoted automatically'),
 ('hy_ig_spread','credit','BLOCKED_PIT_AND_HISTORY','HY versus IG spread changes'),
 ('yield2y_d3','rates','BLOCKED_PIT','2-year yield 3-session change, availability/revision audit required'),
 ('real10y_d3','rates','BLOCKED_PIT','10-year real yield 3-session change'),
 ('breadth_tail','breadth','BLOCKED_HISTORICAL_UNIVERSE','fraction of stocks breaching own historical downside tail'),
 ('new_low_fraction','breadth','BLOCKED_HISTORICAL_UNIVERSE','fraction of stocks making 20-session lows'),
 ('event_next','events','BLOCKED_KNOWN_AT_CALENDAR','CPI/NFP/FOMC decision next session; calendar known before cutoff'),
 ('event_in5','events','BLOCKED_KNOWN_AT_CALENDAR','same three events within next5 sessions; distinguish from event-day override'),
 ('es_overnight','premarket','BLOCKED_TIMESTAMPED_SNAPSHOTS','ES return and range at 09:15 America/New_York; separate update model'),
 ('nq_relative','premarket','BLOCKED_TIMESTAMPED_SNAPSHOTS','NQ vs ES overnight return at same cutoff')]
NAMES=[r[0] for r in REGISTRY]

def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
def safe(root,rel):
 p=PurePosixPath(rel)
 if p.is_absolute() or '..' in p.parts:raise ValueError('UNSAFE_RELATIVE_PATH:'+rel)
 q=root.joinpath(*p.parts)
 # Only task descendants: macOS /var and /tmp ancestor aliases are legitimate.
 cur=root
 for part in p.parts:
  cur=cur/part
  if cur.is_symlink():raise ValueError('DESCENDANT_SYMLINK:'+rel)
 return q

def write(p,b):
 p.parent.mkdir(parents=True,exist_ok=True)
 if p.is_symlink():raise ValueError('OUTPUT_SYMLINK')
 with p.open('xb') as f:f.write(b)
def dump(p,x):write(p,(json.dumps(x,ensure_ascii=False,indent=2,sort_keys=True,allow_nan=False)+'\n').encode())
def rows(p):
 with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def csvwrite(p,rs,fields=None):
 rs=list(rs);fields=fields or list(dict.fromkeys(k for r in rs for k in r)) or ['empty']
 s=io.StringIO(newline='');w=csv.DictWriter(s,fieldnames=fields);w.writeheader()
 for r in rs:w.writerow({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(dict,list)) else v for k,v in r.items()})
 write(p,s.getvalue().encode('utf-8-sig'))
def avg(x):return sum(x)/len(x) if x else None
def quant(x,q):
 if not x:return None
 x=sorted(x);j=(len(x)-1)*q;i=int(j);return x[i]+(x[min(i+1,len(x)-1)]-x[i])*(j-i)
def rank(x):
 order=sorted(range(len(x)),key=x.__getitem__);out=[0.]*len(x);i=0
 while i<len(x):
  j=i+1
  while j<len(x) and x[order[j]]==x[order[i]]:j+=1
  for k in range(i,j):out[order[k]]=(i+j-1)/2
  i=j
 return out
def corr(x,y):
 if len(x)<3:return None
 a=avg(x);b=avg(y);xx=sum((v-a)**2 for v in x);yy=sum((v-b)**2 for v in y)
 return sum((u-a)*(v-b) for u,v in zip(x,y))/math.sqrt(xx*yy) if xx>1e-20 and yy>1e-20 else None
def spearman(x,y):return corr(rank(x),rank(y))
def partial(x,y,v):
 x,y,v=rank(x),rank(y),rank(v);a=corr(x,y);b=corr(x,v);c=corr(y,v)
 if None in (a,b,c) or (1-b*b)*(1-c*c)<1e-12:return None
 return max(-1.,min(1.,(a-b*c)/math.sqrt((1-b*b)*(1-c*c))))
def block_ci(ids,x,y,reps=199,block=20):
 # Resample paired, contiguous calendar blocks; rank again in each bootstrap.
 starts=[j for j in range(len(ids)-block+1) if ids[j+block-1]-ids[j]==block-1]
 if len(starts)<20:return [None,None]
 rng=random.Random(3180125+block);out=[]
 for _ in range(reps):
  ix=[]
  while len(ix)<len(ids):
   j=rng.choice(starts);ix.extend(range(j,j+block))
  ix=ix[:len(ids)];c=spearman([x[k] for k in ix],[y[k] for k in ix])
  if c is not None:out.append(c)
 return [quant(out,.05),quant(out,.95)]
def change(v,k):return math.log(v[-1]/v[-1-k])
def zshock(v):
 d=[math.log(b/a) for a,b in zip(v,v[1:])];past=d[-61:-1];s=st.stdev(past)
 return (d[-1]-avg(past))/s if s>1e-12 else None
def streak(d,positive=True):
 n=0
 for v in reversed(d[-5:]):
  if (v>0 if positive else v<0):n+=1
  else:break
 return n

def load_inputs(root,out):
 audit=[];indexpath=safe(root,'config/data-index.json');index=json.loads(indexpath.read_text())
 audit.append({'path':str(indexpath.relative_to(root)),'sha256':sha(indexpath),'role':'index'})
 def readkey(k):
  item=index['files'][k];p=safe(root,item['path'])
  if sha(p)!=item['sha256']:raise ValueError('INDEX_HASH_MISMATCH:'+k)
  audit.append({'path':item['path'],'sha256':item['sha256'],'role':k});return p
 contract=json.loads(readkey('contracts/frozen-data-contract.json').read_text())
 if contract['split']['development']!=['2006-01-01','2018-12-31'] or contract['split']['validation']!=['2019-01-01','2022-12-31']:raise ValueError('SPLIT_CONTRACT_CHANGED')
 dates=[r['date'] for r in rows(readkey('contracts/historical-session-calendar.csv')) if '2006-01-01'<=r['date']<='2022-12-31']
 if dates!=sorted(set(dates)):raise ValueError('CALENDAR_ORDER')
 parent=safe(root,'reports/step2B/MRV-REGRESSION-01')
 manifest=json.loads((parent/'manifest.json').read_text())
 audit.append({'path':str((parent/'manifest.json').relative_to(root)),'sha256':sha(parent/'manifest.json'),'role':'parent_manifest'})
 def parentrows(rel):
  p=safe(parent,rel)
  if manifest.get(rel)!=sha(p):raise ValueError('PARENT_HASH_MISMATCH:'+rel)
  audit.append({'path':str(p.relative_to(root)),'sha256':sha(p),'role':'parent'})
  rr=rows(p);csvwrite(out/'inputs'/Path(rel).name,rr);return rr
 ff={}
 for r in parentrows('inputs/factors.csv'):
  i=int(r['i'])
  if i in ff or i<=0 or i>=len(dates) or dates[i]!=r['target_date'] or dates[i-1]!=r['feature_date']:raise ValueError('FACTOR_ALIGNMENT')
  ff[i]={k:(float(r[k]) if r[k] not in ('','None') else None) for k in BASE}
  if any(v is not None and not math.isfinite(v) for v in ff[i].values()):raise ValueError('NONFINITE_PARENT')
 labs={}
 for r in parentrows('inputs/labels.csv'):
  i=int(r['i']);m=float(r['mae'])
  if i in labs or i not in ff or i+4>=len(dates) or r['target_date']!=dates[i] or r['window_end']!=dates[i+4] or not 0<=m<=1:raise ValueError('LABEL_ALIGNMENT')
  labs[i]={'mae':m,'window_end':r['window_end'],'gap':float(r['gap'])}
 cross=json.loads(readkey('checks/price-crosscheck.json').read_text());bad={}
 for a in ['SPX','NDX']:
  if cross[a]['status'] not in ['PASS','PASS_WITH_QUARANTINE']:raise ValueError('PRICE_QUALITY_NOT_ACCEPTED:'+a)
  bad[a]={r['date'] for r in cross[a]['conflicts']}
 price={};vol={}
 for symbol in ['SPX','NDX','VIX_CLOSE','VVIX_VVIX']:
  obj={};isprice=symbol in ['SPX','NDX']
  for part in ['development','validation']:
   key='research_core/'+part+'/'+symbol+('-ohlc.csv' if isprice else '.csv')
   for r in rows(readkey(key)):
    d=r['date']
    if not '2006-01-01'<=d<='2022-12-31' or d in obj:raise ValueError('CORE_DATE_INVALID:'+symbol)
    if isprice:
     v={k:float(r[k]) for k in ['open','high','low','close']}
     if not all(math.isfinite(x) and x>0 for x in v.values()) or not v['low']<=min(v['open'],v['close'])<=max(v['open'],v['close'])<=v['high']:raise ValueError('OHLC_INVALID')
     obj[d]=v
    else:
     try:v=float(r['value'])
     except (ValueError,TypeError):continue
     if math.isfinite(v) and v>0:obj[d]=v
  if isprice:price[symbol]=obj
  else:vol[symbol]=obj
 # Verify frozen labels directly against accepted OHLC, without touching post-2022 data.
 for i,l in labs.items():
  ds=dates[i-1:i+5]
  if any(d in bad['SPX'] or d not in price['SPX'] for d in ds):raise ValueError('PARENT_LABEL_QUARANTINE')
  p=price['SPX'];m=max(0,1-min(p[d]['low'] for d in dates[i:i+5])/p[dates[i]]['open'])
  if abs(m-l['mae'])>1e-10:raise ValueError('PARENT_LABEL_REPRODUCTION')
 return dates,ff,labs,price,vol,bad,audit

def features(dates,ff,price,vol,bad,extra):
 result={}
 for i,b in sorted(ff.items()):
  f={k:None for k in NAMES};f.update(b);ds=dates[max(0,i-70):i];t=dates[i-1]
  for sym,prefix in [('VIX_CLOSE','vix'),('VVIX_VVIX','vvix')]:
   vals=[vol[sym].get(d) for d in ds]
   if len(vals)==70 and all(v is not None for v in vals):
    f[prefix+'_d1']=change(vals,1);f[prefix+'_shock']=zshock(vals)
    if prefix=='vix':
     f['vix_d3']=change(vals,3);f['vix_accel']=change(vals,3)-math.log(vals[-4]/vals[-7])
     f['vix_rise_run']=streak([b-a for a,b in zip(vals,vals[1:])])
  if len(ds)==70 and all(d in price['SPX'] and d not in bad['SPX'] for d in ds):
   p=[price['SPX'][d] for d in ds];c=[v['close'] for v in p];r=[math.log(b/a) for a,b in zip(c,c[1:])]
   s1=st.stdev(r[-61:-1]);s3=st.stdev(r[-63:-3]);s6=st.stdev(r[-66:-6])
   f['spx_down_z1']=-r[-1]/s1 if s1>1e-12 else None
   f['spx_down_z3']=-sum(r[-3:])/(s3*math.sqrt(3)) if s3>1e-12 else None
   f['spx_down_accel']=-(sum(r[-3:])-sum(r[-6:-3]))/(s6*math.sqrt(3)) if s6>1e-12 else None
   f['spx_down_run']=streak(r,False);ranges=[(v['high']-v['low'])/old['close'] for old,v in zip(p,p[1:])]
   den=avg(ranges[-21:-1]);f['spx_range_burst']=ranges[-1]/den if den>1e-12 else None
   v=p[-1];f['spx_close_weak']=(v['high']-v['close'])/(v['high']-v['low']) if v['high']>v['low'] else None
   f['spx_gap_down']=-math.log(v['open']/p[-2]['close'])
  if len(ds)>=4 and all(d in price[a] and d not in bad[a] for a in ['SPX','NDX'] for d in ds):
   f['ndx_weak3']=math.log(price['SPX'][t]['close']/price['SPX'][ds[-4]]['close'])-math.log(price['NDX'][t]['close']/price['NDX'][ds[-4]]['close'])
  for sym,name,invert in [('VIX9D','term9',False),('VIX3M','term3m',True)]:
   def term(d):
    a=extra[sym].get(d);v=vol['VIX_CLOSE'].get(d)
    return ((-1 if invert else 1)*math.log(a/v)) if a and v else None
   f[name]=term(t)
   q=[term(d) for d in ds[-4:]]
   if len(q)==4 and all(v is not None for v in q):f[name+'_d3']=q[-1]-q[0]
  f['skew']=extra['SKEW'].get(t);q=[extra['SKEW'].get(d) for d in ds[-6:]]
  if len(q)==6 and all(v is not None for v in q):f['skew_d5']=q[-1]-q[0]
  if any(v is not None and not math.isfinite(v) for v in f.values()):raise ValueError('NONFINITE_FEATURE')
  result[i]=f
 return result

def split(ids,dates,labs,start,end):
 first=bisect.bisect_left(dates,start)
 return [i for i in ids if start<=dates[i]<=end and labs[i]['window_end']<=end and i>=first+5]
def events(ids,labs):
 clusters=[]
 for i in ids:
  if labs[i]['mae']<=SEVERE:continue
  if clusters and i<=clusters[-1]['end']:clusters[-1]['end']=i+4
  else:clusters.append({'start':i,'end':i+4})
 return clusters

def alarm_metrics(ids,alarm,labs,allids,dates):
 lookup=dict(zip(ids,alarm));ev=[]
 for c in events(allids,labs):
  s=c['start'];win=list(range(s-4,s+1));ok=all(i in lookup for i in win)
  hit=any(lookup.get(i,False) for i in win) if ok else None
  ev.append({'event_start':dates[s],'event_end':dates[c['end']],'observable':ok,'hit':hit})
 mid=[i for i in ids if MODERATE<labs[i]['mae']<=SEVERE];low=[i for i in ids if labs[i]['mae']<=MODERATE];sev=[i for i in ids if labs[i]['mae']>SEVERE]
 observed=[e for e in ev if e['observable']]
 return {'n':len(ids),'alarm_fraction':avg([int(v) for v in alarm]),'moderate_n':len(mid),'moderate_to_severe':avg([int(lookup[i]) for i in mid]),'low_n':len(low),'low_to_severe':avg([int(lookup[i]) for i in low]),'severe_windows':len(sev),'severe_window_recall':avg([int(lookup[i]) for i in sev]),'events_total':len(ev),'events_observable':len(observed),'events_missed':sum(not e['hit'] for e in observed),'events_unobservable':len(ev)-len(observed)},ev

def assoc(ids,f,labs,key,bootstrap=True):
 x=[f[i][key] for i in ids];y=[labs[i]['mae'] for i in ids];v=[f[i]['vix'] for i in ids]
 return {'n':len(ids),'spearman_mae':spearman(x,y),'partial_spearman_given_vix':partial(x,y,v),'ci90_block20':block_ci(ids,x,y) if bootstrap else [None,None]}

def study(dates,f,labs,out):
 allids=sorted(i for i in labs if all(f[i][k] is not None for k in BASE))
 devall=split(allids,dates,labs,'2007-01-01','2018-12-31');valall=split(allids,dates,labs,'2019-01-01','2022-12-31')
 summary=[];annual=[];all_events=[];thresholds=[];curves=[];elig=[]
 for number,(key,group,formula) in enumerate(REGISTRY,1):
  print('FACTOR %d/%d %s'%(number,len(REGISTRY),key),flush=True)
  tr=[i for i in devall if f[i][key] is not None];te=[i for i in valall if f[i][key] is not None]
  coverage={'factor':key,'group':group,'development_n':len(tr),'validation_n':len(te),'development_coverage':len(tr)/len(devall),'validation_coverage':len(te)/len(valall),'first_feature_date':dates[tr[0]-1] if tr else None,'last_target_date':dates[te[-1]] if te else None}
  if len(tr)<500 or len(te)<200:
   summary.append(dict(coverage,status='INSUFFICIENT_DATA'));continue
  a=assoc(tr,f,labs,key);b=assoc(te,f,labs,key)
  rho=a['spearman_mae'];direction=1 if rho is None or rho>=0 else -1
  ys=[]
  for year in range(2007,2023):
   ids=split(tr if year<=2018 else te,dates,labs,str(year)+'-01-01',str(year)+'-12-31')
   if len(ids)<20:continue
   ar=assoc(ids,f,labs,key,False);annual.append(dict(factor=key,year=year,**ar));
   if year>=2019 and ar['spearman_mae'] is not None:ys.append(direction*ar['spearman_mae']>0)
  ci=b['ci90_block20'];sign_consistent=(rho is not None and b['spearman_mae'] is not None and rho*b['spearman_mae']>0)
  # Exploratory screen: no claim of multiplicity-adjusted significance or model acceptance.
  signal=bool(rho is not None and abs(rho)>=.05 and sign_consistent and abs(b['spearman_mae'])>=.03)
  row=dict(coverage,status='CORRELATION_CANDIDATE' if signal else 'WEAK_OR_UNSTABLE',development_rho=rho,validation_rho=b['spearman_mae'],validation_ci90_low=ci[0],validation_ci90_high=ci[1],validation_partial_vix=b['partial_spearman_given_vix'],development_ci90=a['ci90_block20'],validation_positive_direction_years=sum(ys),validation_years=len(ys),direction_from_development=direction,ci_excludes_zero=bool(ci[0] is not None and (ci[0]>0 or ci[1]<0)))
  # All five offsets: nonoverlapping-window descriptive sensitivity.
  for offset in range(5):
   ids=[i for i in te if i%5==offset];elig.append({'factor':key,'offset':offset,'n':len(ids),'rho':spearman([f[i][key] for i in ids],[labs[i]['mae'] for i in ids])})
  for budget in [.10,.20,.30]:
   bound=quant([direction*f[i][key] for i in tr],1-budget);vbound=quant([f[i]['vix'] for i in tr],1-budget)
   for kind,alerts in [('factor',[direction*f[i][key]>bound for i in te]),('matched_vix',[f[i]['vix']>vbound for i in te])]:
    m,ev=alarm_metrics(te,alerts,labs,valall,dates);curves.append(dict(factor=key,reference=kind,development_alarm_budget=budget,**m))
    if budget==.20:
     if kind=='factor':row.update({'alarm_fraction':m['alarm_fraction'],'moderate_to_severe':m['moderate_to_severe'],'events_observable':m['events_observable'],'events_missed':m['events_missed'],'events_unobservable':m['events_unobservable']})
     all_events.extend(dict(factor=key,reference=kind,**e) for e in ev)
   thresholds.append({'factor':key,'budget':budget,'direction':direction,'threshold':bound,'matched_vix_threshold':vbound,'fitted_on':'2007-2018 available matched dates','ties':'strict >; no random tie splitting'})
  summary.append(row)
 csvwrite(out/'factor-summary.csv',summary);csvwrite(out/'annual.csv',annual);csvwrite(out/'alarm-curves.csv',curves)
 csvwrite(out/'event-diagnostics.csv',all_events);csvwrite(out/'thresholds.csv',thresholds);csvwrite(out/'nonoverlap-sensitivity.csv',elig)
 # Redundancy screening on development only. Optional shortlist, at most 2/group and 8 new factors.
 selected=[];redundancy=[]
 for row in sorted([r for r in summary if r['status']=='CORRELATION_CANDIDATE' and r['group']!='baseline'],key=lambda r:(-abs(r['development_rho']),r['factor'])):
  key=row['factor'];group=row['group'];duplicate=False
  for other in selected:
   ids=[i for i in devall if f[i][key] is not None and f[i][other] is not None]
   r=spearman([f[i][key] for i in ids],[f[i][other] for i in ids]) if len(ids)>=500 else None
   redundancy.append({'factor':key,'other':other,'n':len(ids),'development_spearman':r})
   if r is not None and abs(r)>.90:duplicate=True
  if not duplicate and len(selected)<8 and sum(next(t[1] for t in REGISTRY if t[0]==k)==group for k in selected)<2:selected.append(key)
 csvwrite(out/'redundancy.csv',redundancy)
 dump(out/'step2B-handoff.json',{'baseline':BASE,'suggested_new_factors':selected,'selection_uses':'development ranking plus already-used 2019-2022 consistency screen; exploratory, not fresh validation','max_new_factors':8,'max_per_group':2,'not_a_leading_model':True,'next_step':'Review coverage and correlation; freeze E1/E2/E3 feature lists before 2B','status':'REVIEW_REQUIRED'})
 return summary,selected

PROTOCOL='''# MRV-step-2A v2.0 与 step-2B 预登记

## 目的与状态
本轮是 step-3 HOLD 后的补充研究。只执行 2A；不运行组合回归，不改变旧结果。
25 个可计算候选（含4个基准），另登记13个缺数据候选。仅研究 SPX 五日风险。
候选定义见 candidate-registry.csv。待补充不等于无效，不计作已检验。
新增数据为 Cboe VIX9D、VIX3M、SKEW 的固定历史快照；仅包含截至2022年数据。
采用保守上市后起点2014/2008/2012，删除上市前回算数据。不前向填充。
这些是现今取得的历史日终数据，不是已验证的历史可得时点快照，也不是盘前数据。
VIX9D/VIX和VIX/VIX3M不是期货期限结构。SKEW不是现实暴跌概率或7日期权尾部概率。

## 统计与时点
前一交易日已完成数据 -> 下一交易日开盘起五个交易日最大不利变动。
严重阈值0.055969989661825176、中等阈值0.026554930513974506沿用冻结版本。
保留原有价格隔离、缺口、标签；不读取2023年及以后行情文件或标签。
开发2007-2018；重复使用的开发验证2019-2022；窗口跨边界删除，段首至少5交易日隔离。
统计为 Pearson-rank (Spearman)、控制VIX的偏秩相关、逐年相关、5种不重叠窗口敏感性。
偏相关只是增量线索，不等于对全部原模型的因果或预测增益。
90%区间：199次、20交易日连续块配对重采样，每次重新排名；探索性区间未做多重检验修正。
筛选线索：开发 |rho|>=0.05，验证 |rho|>=0.03 且同号；不要求单因子成为完整预测模型。
每组最多2个、总计最多8个新增建议；按开发相关排序，开发样本|相关|>0.90的候选去重。
完整结果全部保留，未入选不是证明无效。此筛选及阈值为本轮预登记，不根据结果更改。
报警诊断：方向和10/20/30%报警分位阈值只由开发集决定；验证报警占比不承诺等于预算。
每个因子与VIX在相同日期比较；不是旧L_G5成绩复现。不能跨不同样本直接排优劣。
严重事件：合并重叠的严重五日窗口；首次窗口前4个目标日及该日共5次预测观察。
若5次预测任一缺失，事件记unobservable，而非漏报或命中；分母必须同时报告。
后来的事件日覆盖不能消除早期漏报。中等风险升级率分母是真实中等风险日。
逐因子结果属于探索，不能宣称50%过报已解决或总体风险通过。

## 待补数据
信用、利率等旧reference数据不转为预测输入；不使用最新修订宏观历史冒充PIT。
流动性需要真实价差/成交额，市场宽度需要历史成分，周度期权需要历史期权链。
事件仅CPI/NFP/FOMC决议，需当时已知日历，事件日覆盖单独留痕。
盘前研究冻结09:15 America/New_York（自动处理DST），需该时点及之前的原始行情快照。
18:00台湾主报告和09:15美东更新分别评估，不混为一个发布时间。
隔夜已发生损失与开盘后的风险分开；现有五日目标不含进入窗口前跳空。
本版不自动下载未知供应商、购买数据或建立伪盘前代理；后续补源后升版运行。

## 2B有限比较方案（本脚本不执行）
基准：冻结L_G5原版、VIX基准、同训练窗口的四因子Logit重拟合。
E1：四因子 + 2A选出的速度/路径信息，正则化Logit。
E2：E1 + 有合格覆盖的新增期权期限/偏斜或未来补齐的信用/流动性信息，正则化Logit。
E3：与E2相同输入，增加受限非线性（每个新增因子最多2个训练分位折点）及最多2个预先登记交互。
缺少新信息时E2/E3记BLOCKED，不复制E1凑模型数量。
正则强度仅{0.01,0.1}，开发期滚动选择；每族最多2个配置，不广搜全部组合。
先做开发期扩展窗口检验；2019-2020校准报警阈值；2021-2022作已知历史压力复查，不能称新独立测试。
2A已经查看2019-2022，2B不得伪称其对因子选择独立。
同时报告：事件漏报数/分母、预警提前量、中等升级、低风险升级、报警日占比、最长连续报警、逐年和逐事件结果。
对比10/20/30%校准预算，主比较20%；相同日期、相同目标、同一时间边界；剔除组别做消融。
不得靠降低阈值并长期严重报警宣称改进；同时检查漏报与过报的权衡及时间块不确定性。
用户目标是严重事件零漏报、限制中等升级；零漏报属于目标，少量样本零漏报不等于可靠保证。
本轮预登记的历史候选筛选参考：相对匹配四因子基准至少少漏1个可观察事件，
中等升级率至少下降5个百分点，报警日占比不增加；至少2个有严重事件的年份支持改善。
这些是候选筛选门槛，不是实盘验收标准；没有方案通过则leading=None，保持HOLD。
事件日直接严重为单独策略覆盖，对同一候选报告覆盖前后成绩，不能改真实标签。
2023-2025既往已经使用，只能称复查；真正新证据依赖冻结后未用于选择的数据和前瞻留档。
最后由用户审阅2A，冻结候选再执行2B；本脚本不会自动进入step-3/4或改交易引擎。
'''

def selftest():
 passed=[]
 def ck(name,yes):
  if not yes:raise AssertionError(name)
  passed.append(name)
 ck('tie_ranks',rank([2,1,2])==[1.5,0.,1.5]);ck('perfect_rank',abs(spearman([1,2,3],[3,4,9])-1)<1e-12)
 ck('constant_missing',spearman([1,1,1],[2,3,4]) is None);ck('strict_quantile',quant([0,1,2],.5)==1)
 ck('signed_changes',abs(change([1,2,4,8],3)-math.log(8))<1e-12);ck('streak_reset',streak([1,-1,1,1])==2)
 ck('down_streak',streak([-1,-2],False)==2);ck('partial_collinear',partial([1,2,3],[1,3,2],[1,2,3]) is None)
 with tempfile.TemporaryDirectory() as tmp:
  root=Path(tmp).resolve();write(safe(root,'a/b'),b'a');ck('mac_alias_safe',safe(root,'a/b').read_bytes()==b'a')
  try:safe(root,'../outside');ok=False
  except ValueError:ok=True
  ck('path_traversal_rejected',ok);(root/'link').symlink_to(root/'a',target_is_directory=True)
  try:safe(root,'link/b');ok=False
  except ValueError:ok=True
  ck('descendant_symlink_rejected',ok)
 dates=[(dt.date(2010,1,1)+dt.timedelta(days=i)).isoformat() for i in range(100)]
 labs={i:{'mae':.10 if i in [30,34,60] else .01,'window_end':dates[i+4]} for i in range(90)}
 ck('overlap_events',events(list(range(90)),labs)==[{'start':30,'end':38},{'start':60,'end':64}])
 ids=list(range(20,80));alerts=[i==28 for i in ids];m,e=alarm_metrics(ids,alerts,labs,ids,dates)
 ck('early_warning',m['events_missed']==1 and e[0]['hit']);ids.remove(59);m,e=alarm_metrics(ids,[False]*len(ids),labs,list(range(20,80)),dates)
 ck('missing_warning_not_miss',m['events_unobservable']==1 and m['events_observable']==1)
 ids=split(list(labs),dates,labs,'2010-02-01','2010-02-28');ck('purged_end',all(labs[i]['window_end']<='2010-02-28' for i in ids));ck('embargo_start',min(ids)>=36)
 ci=block_ci(list(range(100)),list(range(100)),list(range(100)),19);ck('block_interval',ci[0]>.99)
 # Future perturbation invariant for all newly constructed factors.
 d=[str(i) for i in range(100)];p={a:{x:{'open':100+i,'close':101+i,'high':103+i,'low':99+i} for i,x in enumerate(d)} for a in ['SPX','NDX']};v={s:{x:20+i*.1 for i,x in enumerate(d)} for s in ['VIX_CLOSE','VVIX_VVIX']};extra={s:{x:30+i*.1 for i,x in enumerate(d)} for s in ['VIX9D','VIX3M','SKEW']};bad={'SPX':set(),'NDX':set()};ff={80:dict(zip(BASE,[1.,2.,3.,4.]))}
 a=features(d,ff,p,v,bad,extra)
 for asset in p:
  for x in d[80:]:p[asset][x]={k:9999 for k in p[asset][x]}
 for series in list(v.values())+list(extra.values()):
  for x in d[80:]:series[x]=99999
 ck('no_future_feature_leakage',a==features(d,ff,p,v,bad,extra));v['VIX_CLOSE'].pop(d[78]);b=features(d,ff,p,v,bad,extra);ck('missing_not_bridged',b[80]['vix_d1'] is None)
 ck('candidate_budget',len(NAMES)==25 and len(set(NAMES))==25)
 return {'status':'PASS','count':len(passed),'tests':passed}

def finalize(out):
 files={str(p.relative_to(out)):sha(p) for p in sorted(out.rglob('*')) if p.is_file() and p.name not in ['manifest.json','evidence.zip']}
 dump(out/'manifest.json',files)
 with zipfile.ZipFile(out/'evidence.zip','x',zipfile.ZIP_DEFLATED) as z:
  for rel in list(files)+['manifest.json']:z.write(out/rel,rel)
 print('RESULT_ROOT='+str(out)+'\nEVIDENCE='+str(out/'evidence.zip'),flush=True)

def run(root,out,bundle,preflight=False):
 tests=selftest();dump(out/'package-tests.json',tests);print('PACKAGE_SELFTEST=PASS %d/%d'%(tests['count'],tests['count']),flush=True)
 write(out/'protocol.md',PROTOCOL.encode());dump(out/'registration.json',{'version':VERSION,'severe':SEVERE,'moderate':MODERATE,'registry':REGISTRY,'pending':PENDING,'hold_state':'HOLD','created_before_analysis':True,'bootstrap_reps':199,'block_length':20,'past_validation_reused':True})
 extra={};csvwrite(out/'candidate-registry.csv',[{'factor':k,'group':g,'formula':formula,'status':'SCHEDULED','source_class':'DAILY_EOD_PROXY'} for k,g,formula in REGISTRY]+[{'factor':k,'group':g,'formula':desc,'status':status,'source_class':'NOT_TESTED'} for k,g,status,desc in PENDING])
 dump(out/'new-source-provenance.json',bundle['sources'])
 for sym,blob in bundle['data'].items():
  b=base64.b64decode(blob);p=out/'inputs'/(sym+'.csv');write(p,b)
  if hashlib.sha256(b).hexdigest()!=bundle['sources'][sym]['included_sha256']:raise ValueError('BUNDLED_DATA_HASH')
  rr=rows(p);extra[sym]={}
  for r in rr:
   d=r['date'];v=float(r['value'])
   if d in extra[sym] or not bundle['sources'][sym]['use_from']<=d<='2022-12-31' or not math.isfinite(v) or v<=0:raise ValueError('BUNDLED_SERIES_INVALID')
   extra[sym][d]=v
 dates,ff,labs,price,vol,bad,audit=load_inputs(root,out)
 f=features(dates,ff,price,vol,bad,extra)
 dump(out/'input-audit.json',audit)
 csvwrite(out/'features.csv',[dict(i=i,target_date=dates[i],feature_date=dates[i-1],**v) for i,v in sorted(f.items())])
 csvwrite(out/'coverage.csv',[{'factor':k,'available_feature_rows':sum(v[k] is not None for v in f.values()),'total_feature_rows':len(f),'first_available':next((dates[i-1] for i in sorted(f) if f[i][k] is not None),None)} for k in NAMES])
 dump(out/'runtime.json',{'python':sys.version,'platform':platform.platform(),'standard_library_only':True,'network_calls':0,'analysis_mode':'preflight' if preflight else 'research'})
 if preflight:
  dump(out/'result.json',{'engineering':'PASS','state':'PREFLIGHT_ONLY','factor_analysis_executed':False,'risk_acceptance':'HOLD','feature_rows':len(f),'label_rows':len(labs)})
  write(out/'REPORT.md','真实输入预检通过；未执行实际因子筛选，未形成有效性结论。\n'.encode())
 else:
  summary,selected=study(dates,f,labs,out)
  result={'engineering':'PASS','state':'COMPLETE_WITH_DECLARED_DATA_GAPS','risk_acceptance':'HOLD','factor_candidates':len(NAMES),'pending_candidates':len(PENDING),'suggested_for_2B':selected,'step3_status':'PREVIOUS_HOLD_UNCHANGED','production_changed':False,'new_data_class':'CURRENT_HISTORY_EOD_PROXY_NOT_PIT'}
  dump(out/'result.json',result)
  lines=['# MRV-step-2A v2.0 研究结果','','工程完成；模型有效性仍为 HOLD。','', '本轮运行25个单因子候选，另13项因数据缺口未检验。没有运行2B组合模型。', '', '新增期权指数是历史日终代理；不是历史盘前快照。2019—2022已重复用于研究。', '', '## 待复核的2B输入建议', '', ', '.join(selected) or '无候选达到本轮探索性筛选条件。', '', '## 完整单因子结果', '', '| 因子 | 开发相关 | 验证相关 | 验证报警占比 | 中等升级率 | 漏报/可观察事件 | 状态 |', '|---|---:|---:|---:|---:|---|---|']
  def fmt(v):return 'NA' if v is None else '%.4f'%v
  for r in summary:lines.append('|%s|%s|%s|%s|%s|%s/%s|%s|'%(r['factor'],fmt(r.get('development_rho')),fmt(r.get('validation_rho')),fmt(r.get('alarm_fraction')),fmt(r.get('moderate_to_severe')),r.get('events_missed','NA'),r.get('events_observable','NA'),r['status']))
  lines+=['','报警分位预算来自开发期20%，实际验证报警比例可能明显偏离；不同因子缺失率不同，不得跨行直接比较优劣。','事件分母为完整5次观察的事件，缺失事件见 event-diagnostics.csv；不是直接复现此前5/11。','区间未经多重检验校正，仅供探索；强相关、有效性、实盘适用性均需后续证明。','完整2B设计见protocol.md；预登记缺数据项目见candidate-registry.csv。','请回传 evidence.zip；没有自动修改旧2A/2B/step-3状态或进入交易流程。']
  write(out/'REPORT.md',('\n'.join(lines)+'\n').encode())
 for r in audit:
  if sha(safe(root,r['path']))!=r['sha256']:raise ValueError('INPUT_CHANGED_DURING_RUN:'+r['path'])
 print('MRV_STEP_2A_V2=PASS\nRISK_ACCEPTANCE=HOLD',flush=True)
