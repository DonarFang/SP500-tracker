import math,statistics as st,json,base64,hashlib,sys,platform
from decimal import Decimal
VERSION='MRV-step-2A-Daily-v1.0'
NEW=[('spx_down'+str(k),'price_change','negative '+str(k)+' session log return') for k in [1,3,5,10,20]]+[
 ('spx_rv5','vol_level','annualized 5-session realized volatility'),('spx_rv20','vol_level','annualized 20-session realized volatility'),('spx_rv60','vol_level','annualized 60-session realized volatility'),
 ('spx_dd20','price_state','1-close/maximum last20 closes'),('spx_dd60','price_state','1-close/maximum last60 closes'),('spx_ma20_gap','price_state','1-close/mean last20 closes'),
 ('spx_downside20','price_path','sqrt(mean squared negative returns, last20)'),('spx_range','price_path','latest high-low / previous close'),('spx_tail_today','price_path','latest prior close to low loss'),('spx_tail_max5','price_path','maximum prior-close-to-low loss over last5'),
 ('vix_level_raw','vol_level','VIX raw level'),('vvix_level','vol_of_vol','VVIX raw level'),('vix_rv20','option_term','log((VIX/100)/RV20)'),
 ('ndx_down1','cross_index','negative 1-session NDX log return'),('ndx_down5','cross_index','negative 5-session NDX log return'),('ndx_spx_weak5','cross_index','SPX 5-session return minus NDX 5-session return'),
 ('ix_vix_down3','interaction','log(VIX) * SPX negative3 return'),('ix_term9_range','interaction','log(VIX9D/VIX) * SPX range burst'),('ix_term3_down3','interaction','log(VIX/VIX3M) * SPX down z3'),('ix_range_weak','interaction','SPX range burst * close weakness')]
FAMILIES=[('M1','regularized logistic','severe vs rest; sparse multi-factor'),('M2','ordinal logistic','joint moderate-or-severe and severe thresholds'),('M3','two-stage logistic','moderate-or-severe probability times conditional severe probability'),('M4','bounded additive splines','at most2 training-only knots per selected factor'),('M5','shallow tree ensemble','bounded depth and leaf size; no date features'),('M6','conditional downside quantile','forecast quantiles of daily downside loss'),('M7','complementary experts','volatility/price/options expert combination'),('M8','false-alarm filter','time-out-of-fold base alarms, filtered under severe recall constraint')]
PROTOCOL='''# MRV single-day 2A v1.0
Prediction: after T close, features dated no later than T, target next exchange session. No premarket inputs. EOD histories are historical proxies, not verified exact release-time snapshots; no certified 16:00 PIT claim.
Label D=max(0,1-L_next/C_T), based on SPX regular-session OHLC. Severe D>=.03; moderate .012<D<.03; light D<=.012. Decimal comparisons decide boundary membership. No overlapping event merging or early-window credit. Each actual severe day is a separate denominator member.
Existing indexed input hashes and price quarantine enforced. Old 5-day labels are read only to verify prior data lineage; new daily labels are rebuilt independently for all eligible calendar dates, including final sessions and year boundaries. No forward fill or interpolation. No production writes.
Development 2007-2018: screen per factor on its available rows; minimum500 rows and10 severe days. Direction from development severe AUC. Check expanding-year2016,2017,2018 diagnostics using earlier years only to determine direction. Candidate signal: abs(Spearman)>=.05 OR oriented severe AUC>=.60 OR severe-v-moderate AUC>=.55; at least2 rolling years AUC>=.50. Ranking: severe-v-moderate AUC, severe AUC, abs rho; max3 per family, max12; pairwise abs Spearman>.90 on>=250 common development rows prunes duplicates. Screening is exploratory, not significance proof; no p-value/multiple-testing claims.
Calibration2019-2020: for every factor test exactly8 directional thresholds (score quantiles .50,.60,.70,.80,.90,.95,.975,.99). Exclude all CPI/NFP/scheduled FOMC dates from BOTH moderate false-positive numerator and denominator. Require moderate false-positive<=.20 and non-event severe observations>0. Choose maximum non-event severe recall, then fewer light false alarms, fewer alarms, more restrictive threshold. If infeasible: BLOCKED; no evaluation fallback. Missing values remain unavailable, never silently counted as safe. Official false-positive rate is null when any relevant non-event class row lacks a prediction; observed-only rate is separately named, never substituted for acceptance.
Review2021-2022: frozen direction and threshold, no selection or retuning. All periods already used historically; NOT independent validation. Shortlist is DEVELOPMENT ONLY, not evaluation-ranked. Refit/combination/model family testing belongs to2B. M1-M8 are preregistered structures NOT fitted or endorsed in2A.
Calendar proxy only covers2019-2022; earlier development event status UNKNOWN, never assume non-event. Development has AUC/correlation diagnostics but no event-excluded acceptance score. All actual severe dates in2019-2022 retained in full-calendar coverage audit; missing labels and missing features reported. Per-factor metrics differ in coverage; common-shortlist-cohort.csv is provided for fair2B cohorts; never compare different denominators as equally strong evidence.
Calendar actual dates verified in prior package; historical prior-known calendar snapshots NOT verified. Event override only the scheduled release date, not day after; no holiday shift; no emergency FOMC. Overridden event days excluded from false-positive denominators even if model also signals; all actual severe event days remain in final recall. All-day and non-event recall and availability reported separately. Missing non-event severe predictions count as missed in full-cohort strict recall. Report model-only recall too.
Final2B goal:0/N severe missed with N>0, non-event moderate false-positive<=20%; report light false-positive, alarm fraction, longest run, per-year and missing coverage. No certification or leading model in2A. Existing step3 HOLD unchanged.
'''
def label(prev,low):
 d=max(Decimal(0),Decimal(1)-Decimal(str(low))/Decimal(str(prev)))
 return float(d),'severe' if d>=Decimal('.03') else 'moderate' if d>Decimal('.012') else 'light'
def auc(xs,ys,c):
 n=sum(ys);m=len(ys)-n
 if not n or not m:return None
 ranks=c.rank(xs)
 return (sum(r+1 for r,y in zip(ranks,ys) if y)-n*(n+1)/2)/(n*m)
def make_features(dates,price,vol,bad,extra,c):
 base={}
 for i in range(70,len(dates)):
  ds=dates[i-70:i];f={k:None for k in c.BASE};v=vol['VIX_CLOSE'];t=ds[-1]
  if v.get(t):f['vix']=math.log(v[t])
  if v.get(t) and v.get(ds[-6]):f['vix_delta5']=math.log(v[t]/v[ds[-6]])
  if all(d in price['SPX'] and d not in bad['SPX'] for d in ds):
   rr=[math.log(price['SPX'][b]['close']/price['SPX'][a]['close']) for a,b in zip(ds,ds[1:])]
   rv={k:st.stdev(rr[-k:])*math.sqrt(252) for k in [5,20,60]}
   if min(rv.values())>0:f['rv5_20']=math.log(rv[5]/rv[20]);f['rv20_60']=math.log(rv[20]/rv[60])
  base[i]=f
 fs=c.features(dates,base,price,vol,bad,extra)
 for i,f in fs.items():
  f.update({k:None for k,g,desc in NEW});ds=dates[i-70:i];t=ds[-1]
  if all(d in price['SPX'] and d not in bad['SPX'] for d in ds):
   p=[price['SPX'][d] for d in ds];cl=[x['close'] for x in p];r=[math.log(b/a) for a,b in zip(cl,cl[1:])]
   for k in [1,3,5,10,20]:f['spx_down'+str(k)]=-sum(r[-k:])
   for k in [5,20,60]:f['spx_rv'+str(k)]=st.stdev(r[-k:])*math.sqrt(252)
   for k in [20,60]:f['spx_dd'+str(k)]=1-cl[-1]/max(cl[-k:])
   f['spx_ma20_gap']=1-cl[-1]/c.avg(cl[-20:]);f['spx_downside20']=math.sqrt(c.avg([min(x,0)**2 for x in r[-20:]]))
   f['spx_range']=(p[-1]['high']-p[-1]['low'])/cl[-2];loss=[label(a['close'],b['low'])[0] for a,b in zip(p,p[1:])]
   f['spx_tail_today']=loss[-1];f['spx_tail_max5']=max(loss[-5:])
  f['vix_level_raw']=vol['VIX_CLOSE'].get(t);f['vvix_level']=vol['VVIX_VVIX'].get(t)
  if f['vix_level_raw'] and f['spx_rv20']:f['vix_rv20']=math.log(f['vix_level_raw']/100/f['spx_rv20'])
  nd=ds[-6:]
  if all(d in price['NDX'] and d not in bad['NDX'] for d in nd):
   n=[price['NDX'][d]['close'] for d in nd];f['ndx_down1']=-math.log(n[-1]/n[-2]);f['ndx_down5']=-math.log(n[-1]/n[0])
   if f['spx_down5'] is not None:f['ndx_spx_weak5']=f['ndx_down5']-f['spx_down5']
  for k,a,b in [('ix_vix_down3','vix','spx_down3'),('ix_term9_range','term9','spx_range_burst'),('ix_term3_down3','term3m','spx_down_z3'),('ix_range_weak','spx_range_burst','spx_close_weak')]:
   if f[a] is not None and f[b] is not None:f[k]=f[a]*f[b]
  if any(v is not None and not math.isfinite(v) for v in f.values()):raise ValueError('NONFINITE_FACTOR')
 return fs

def describe(ids,key,fs,labs,c,direction=1):
 ix=[i for i in ids if fs.get(i,{}).get(key) is not None];x=[direction*fs[i][key] for i in ix];y=[labs[i]['loss'] for i in ix];sm=[j for j,i in enumerate(ix) if labs[i]['class']!='light']
 return {'n':len(ix),'severe_n':sum(labs[i]['class']=='severe' for i in ix),'rho':c.spearman(x,y) if len(ix)>2 else None,'auc':auc(x,[labs[i]['class']=='severe' for i in ix],c),'auc_severe_vs_moderate':auc([x[j] for j in sm],[labs[ix[j]]['class']=='severe' for j in sm],c)}
def metric(ids,key,fs,labs,event,direction,threshold):
 available={i for i in ids if fs.get(i,{}).get(key) is not None};model={i for i in available if direction*fs[i][key]>threshold};alarms=model|{i for i in ids if event.get(i)}
 sev={i for i in ids if labs[i]['class']=='severe'};non={i for i in ids if not event.get(i)};mid={i for i in non if labs[i]['class']=='moderate'};light={i for i in non if labs[i]['class']=='light'}
 def frac(a,b):return len(a)/len(b) if b else None
 run=best=0;prev=None
 for i in ids:
  run=(run+1 if prev is not None and i==prev+1 else 1) if i in alarms else 0;best=max(best,run);prev=i
 return {'n':len(ids),'available':len(available),'missing':len(ids)-len(available),'severe_n':len(sev),'missed_full':len(sev-alarms),'non_event_severe_n':len(sev&non),'non_event_severe_missed':len((sev&non)-alarms),'model_only_missed':len(sev-model),'severe_missing_features':len(sev-available),'moderate_n':len(mid),'moderate_available_n':len(mid&available),'moderate_false':len(mid&model),'moderate_false_rate':frac(mid&model,mid) if mid<=available else None,'moderate_observed_only_rate':frac(mid&model,mid&available),'light_n':len(light),'light_available_n':len(light&available),'light_false_rate':frac(light&model,light) if light<=available else None,'light_observed_only_rate':frac(light&model,light&available),'alarm_days':len(alarms),'alarm_fraction':frac(alarms,set(ids)),'longest_alarm_run':best}
def choose(ids,key,fs,labs,event,direction,c):
 scores=[direction*fs[i][key] for i in ids if fs.get(i,{}).get(key) is not None];grid=[]
 for q in [.5,.6,.7,.8,.9,.95,.975,.99]:
  th=c.quant(scores,q)
  if th is None:continue
  m=metric(ids,key,fs,labs,event,direction,th);ok=m['moderate_false_rate'] is not None and m['moderate_false_rate']<=.2 and m['non_event_severe_n']>0 and m['available']==m['n']
  grid.append(dict(factor=key,q=q,threshold=th,eligible=ok,**m))
 good=[r for r in grid if r['eligible']]
 return (min(good,key=lambda r:(r['non_event_severe_missed'],r['light_false_rate'] if r['light_false_rate'] is not None else 1,r['alarm_days'],-r['q'])) if good else None),grid

def selftest(c):
 checks=[]
 def ck(n,b):
  if not b:raise AssertionError(n)
  checks.append(n)
 ck('boundary3',label(100,97)[1]=='severe');ck('boundary1_2',label(100,98.8)[1]=='light');ck('middle',label(100,98)[1]=='moderate');ck('gap_included',label(100,95)[0]==.05);ck('rebound_no_close_dependency',label(100,96)[1]=='severe');ck('positive_low_zero',label(100,101)[0]==0)
 ck('auc_ties',auc([1,1],[0,1],c)==.5);ck('auc_perfect',auc([0,1],[0,1],c)==1);ck('auc_no_severe',auc([0,1],[0,0],c) is None)
 fs={i:{'x':float(i)} for i in range(6)};labs={i:{'class':['moderate','moderate','light','severe','severe','light'][i]} for i in fs};events={0:['CPI'],3:['NFP']};m=metric(list(fs),'x',fs,labs,events,1,8)
 ck('event_excluded_both',m['moderate_n']==1 and m['moderate_false']==0);ck('event_severe_retained',m['severe_n']==2 and m['missed_full']==1);ck('no_next_day_override',m['non_event_severe_missed']==1);ck('model_event_separate',m['model_only_missed']==2)
 fs[4]['x']=None;m=metric(list(fs),'x',fs,labs,events,1,0);ck('missing_counts_missed',m['severe_missing_features']==1 and m['missed_full']==1)
 fs[1]['x']=None;fs[2]['x']=None;m=metric(list(fs),'x',fs,labs,events,1,0);ck('missing_moderate_not_safe',m['moderate_false_rate'] is None);ck('missing_light_not_safe',m['light_false_rate'] is None)
 ck('unique_registry',len(set(k for k,g,f in c.REGISTRY+NEW))==len(c.REGISTRY+NEW));ck('eight_model_structures',len(FAMILIES)==8)
 # inherited tests include strict T information cutoff and missing input no interpolation
 parent=c.selftest();return {'status':'PASS','count':len(checks)+parent['count'],'new_checks':checks,'inherited':parent}

def run(root,out,pkg,c,preflight=False):
 tests=selftest(c);c.dump(out/'package-tests.json',tests);print('SELFTEST=PASS',tests['count'],flush=True)
 c.write(out/'protocol.md',PROTOCOL.encode());c.dump(out/'registration.json',{'version':VERSION,'new_factors':NEW,'all_factor_count':len(c.REGISTRY+NEW),'families':FAMILIES,'threshold_quantiles':[.5,.6,.7,.8,.9,.95,.975,.99],'shortlist_max':12,'selection_period':'2007-2018 ONLY','risk_acceptance':'HOLD','independent_validation':False,'price_basis':'previous_close_to_target_regular_session_low'})
 extra={}
 for sym,blob in pkg['bundle']['data'].items():
  b=base64.b64decode(blob)
  if hashlib.sha256(b).hexdigest()!=pkg['bundle']['sources'][sym]['included_sha256']:raise ValueError('SOURCE_HASH')
  p=out/'extra'/ (sym+'.csv');c.write(p,b);extra[sym]={r['date']:float(r['value']) for r in c.rows(p)}
 c.dump(out/'source-provenance.json',pkg['bundle']['sources']);c.dump(out/'calendar.json',pkg['calendar'])
 dates,oldff,oldlabels,price,vol,bad,audit=c.load_inputs(root,out);c.dump(out/'input-audit.json',audit)
 fs=make_features(dates,price,vol,bad,extra,c);labs={};missing=[]
 for i in range(1,len(dates)):
  if dates[i]<'2007-01-01':continue
  if any(d not in price['SPX'] or d in bad['SPX'] for d in [dates[i-1],dates[i]]):missing.append({'date':dates[i],'reason':'SPX_MISSING_OR_QUARANTINED'});continue
  loss,cls=label(price['SPX'][dates[i-1]]['close'],price['SPX'][dates[i]]['low']);labs[i]={'loss':loss,'class':cls}
 evdates={}
 for r in pkg['calendar']['events']:
  if r['event'] not in ['CPI','NFP','FOMC'] or not r['scheduled']:raise ValueError('CALENDAR_INVALID')
  evdates.setdefault(r['date'],[]).append(r['event'])
 event={i:evdates.get(dates[i],[]) for i in labs if '2019-01-01'<=dates[i]<='2022-12-31'}
 c.csvwrite(out/'labels-daily.csv',[dict(i=i,target_date=dates[i],feature_date=dates[i-1],previous_close=price['SPX'][dates[i-1]]['close'],target_low=price['SPX'][dates[i]]['low'],event_status=event.get(i,'UNKNOWN_PRE2019'),**v) for i,v in labs.items()]);c.csvwrite(out/'missing-labels.csv',missing)
 c.csvwrite(out/'features.csv',[dict(i=i,target_date=dates[i],feature_date=dates[i-1],**f) for i,f in fs.items() if i in labs])
 c.csvwrite(out/'factor-registry.csv',[{'factor':k,'group':g,'formula':f,'status':'TESTABLE_EOD_PROXY'} for k,g,f in c.REGISTRY+NEW]+[{'factor':k,'group':g,'formula':f,'status':'EXCLUDED_BY_USER' if g=='premarket' else status} for k,g,status,f in c.PENDING if g!='events'])
 c.csvwrite(out/'model-structures.csv',[{'id':k,'structure':a,'purpose':b,'status':'REGISTERED_FOR_2B_NOT_FITTED'} for k,a,b in FAMILIES]);c.dump(out/'runtime.json',{'version':VERSION,'python':sys.version,'platform':platform.platform(),'offline':True,'premarket':False,'point_in_time_certified':False})
 counts=[]
 for yr in range(2007,2023):
  ix=[i for i in labs if dates[i].startswith(str(yr))];counts.append({'year':yr,'n':len(ix),**{k:sum(labs[i]['class']==k for i in ix) for k in ['severe','moderate','light']},'event_calendar':'KNOWN_PROXY' if yr>=2019 else 'UNAVAILABLE'})
 c.csvwrite(out/'yearly-label-counts.csv',counts)
 if preflight:c.dump(out/'result.json',{'state':'PREFLIGHT_PASS','labels':len(labs),'factors':len(c.REGISTRY+NEW),'no_screening_performed':True,'step3':'HOLD'});return
 dev=[i for i in labs if dates[i]<='2018-12-31'];cal=[i for i in labs if '2019-01-01'<=dates[i]<='2020-12-31'];review=[i for i in labs if '2021-01-01'<=dates[i]<='2022-12-31']
 screen=[];roll=[];grids=[];metrics=[];pred=[];frozen={}
 for n,(key,group,formula) in enumerate(c.REGISTRY+NEW):
  raw=describe(dev,key,fs,labs,c);direction=-1 if raw['auc'] is not None and raw['auc']<.5 else 1;d=describe(dev,key,fs,labs,c,direction);years=0
  for yr in [2016,2017,2018]:
   past=[i for i in dev if dates[i]<str(yr)];now=[i for i in dev if dates[i].startswith(str(yr))];r=describe(past,key,fs,labs,c);sgn=-1 if r['auc'] is not None and r['auc']<.5 else 1;v=describe(now,key,fs,labs,c,sgn);roll.append(dict(factor=key,year=yr,direction=sgn,**v));years+=int(r['n']>=250 and v['severe_n']>=2 and v['auc'] is not None and v['auc']>=.5)
  signal=d['n']>=500 and d['severe_n']>=10 and years>=2 and (abs(d['rho'] or 0)>=.05 or (d['auc'] or 0)>=.6 or (d['auc_severe_vs_moderate'] or 0)>=.55)
  screen.append(dict(factor=key,group=group,direction=direction,rolling_supported_years=years,candidate=signal,**d))
  chosen,grid=choose(cal,key,fs,labs,event,direction,c);grids.extend(grid);frozen[key]={'direction':direction,'threshold':chosen['threshold'] if chosen else None,'state':'CALIBRATED' if chosen else 'BLOCKED_CALIBRATION'}
  if chosen:
   th=chosen['threshold']
   for period,ids in [('calibration',cal),('review',review)]:
    metrics.append(dict(factor=key,period=period,**metric(ids,key,fs,labs,event,direction,th)))
    for yr in sorted({dates[i][:4] for i in ids}):metrics.append(dict(factor=key,period=period+'_'+yr,**metric([i for i in ids if dates[i].startswith(yr)],key,fs,labs,event,direction,th)))
    for i in ids:
     score=fs.get(i,{}).get(key);ma=None if score is None else direction*score>th;pred.append({'factor':key,'period':period,'date':dates[i],'feature_date':dates[i-1],'actual':labs[i]['class'],'event':event[i],'model_alarm':ma,'final_alarm':True if event[i] else ma,'available':score is not None})
  if n%10==0:print('FACTOR_RESEARCH',n+1,'/',len(c.REGISTRY+NEW),flush=True)
 # Development-only selection: do NOT read calibration/review metrics here.
 selected=[];groups={};pruned=[]
 for r in sorted([r for r in screen if r['candidate']],key=lambda r:(-(r['auc_severe_vs_moderate'] or 0),-(r['auc'] or 0),-abs(r['rho'] or 0),r['factor'])):
  k=r['factor'];reason=None
  if len(selected)>=12:reason='BUDGET12'
  elif groups.get(r['group'],0)>=3:reason='GROUP_CAP3'
  else:
   for prev in selected:
    ix=[i for i in dev if fs.get(i,{}).get(k) is not None and fs.get(i,{}).get(prev) is not None]
    if len(ix)>=250 and abs(c.spearman([fs[i][k] for i in ix],[fs[i][prev] for i in ix]) or 0)>.9:reason='REDUNDANT_WITH_'+prev;break
  if reason:pruned.append({'factor':k,'reason':reason})
  else:selected.append(k);groups[r['group']]=groups.get(r['group'],0)+1
 c.dump(out/'shortlist.json',{'selected':selected,'selection_uses':'DEVELOPMENT_ONLY','not_leading_models':True,'pruned':pruned});c.csvwrite(out/'common-shortlist-cohort.csv',[{'i':i,'date':dates[i],'available_all_selected':bool(selected) and all(fs.get(i,{}).get(k) is not None for k in selected)} for i in labs])
 c.csvwrite(out/'development-screen.csv',screen);c.csvwrite(out/'rolling-development.csv',roll);c.csvwrite(out/'calibration-grid.csv',grids);c.csvwrite(out/'alarm-metrics.csv',metrics);c.csvwrite(out/'predictions.csv',pred);c.dump(out/'frozen-single-factor-rules.json',frozen)
 c.dump(out/'result.json',{'state':'COMPLETE','step':'2A','shortlist':selected,'factor_count':len(screen),'model_fits':0,'leading':None,'step3':'PREVIOUS_HOLD_UNCHANGED','risk_acceptance':'HOLD','independent_validation':False,'calendar_prior_known_verified':False})
 lines=['# MRV 单日风险 step-2A','', '标签：昨收到次日最低价；严重≥3%，中等>1.2%且<3%，轻度≤1.2%。无盘前数据。', '发布日从误报分子分母同时排除；全部严重日保留。无提前数日命中替代。', '', '完成 '+str(len(screen))+' 项因子研究；开发期选入 '+str(len(selected))+' 项：'+', '.join(selected), '8类模型结构已登记，尚未拟合。2A不产生leading模型，step3仍HOLD。', '', '年份 | 有效日 | 严重 | 中等 | 轻度','---|---:|---:|---:|---:']
 lines += ['{year}|{n}|{severe}|{moderate}|{light}'.format(**r) for r in counts]
 lines += ['', '请重点查看development-screen、rolling-development、alarm-metrics、missing-labels及shortlist。', '不同因子缺失率不同，必须比较分母；缺失不能当作低风险，校准缺失则BLOCKED。', '单因子不满足零漏报不直接否定组合价值。20%约束用于校准；复查期不保证达标。', '历史EOD及发布日为代理数据，未完成事前可得时点认证；2019以前无发布日日历，不计算排除发布日的误报率。', '既有历史数据已被反复研究，本轮不是独立验证。请回传evidence.zip。']
 c.write(out/'REPORT.md','\n'.join(lines).encode())
