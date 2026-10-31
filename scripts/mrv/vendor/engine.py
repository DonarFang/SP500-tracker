import json,math,random,bisect,statistics,hashlib,sys,platform,datetime
from pathlib import Path
PARENT_HASH='ff5105dcc13e8afabaa4c07df3f3c98b31721a4f27bf6b905772c612e3172836'
MODELS=['M1','M2','M3','M4','M5','M6','M7','M8']
VERSION='MRV-step-2B-Daily-v1.0'
SPECS={'M1':'L2 logistic severe vs rest; lambda=.01','M2':'two cumulative L2 logits P(moderate+),P(severe); monotonic projection; NOT proportional-odds fit','M3':'P(moderate+) times P(severe|moderate+), two L2 logits','M4':'L2 logistic with training-rank hinges at -1/3,+1/3; lambda=.03','M5':'24 bootstrap classification trees; depth3; minleaf30; sqrt(feature count) random features;9 candidate cuts','M6':'24 conditional distribution trees; depth3; minleaf30; leaf-weighted pooled loss distribution; 95th percentile score, NOT probability','M7':'equal mean of three L2 experts: volatility, price state, price path; term factors join volatility','M8':'chronological OOF M1 alarms above training-only80th percentile; logistic false-alarm filter on selected OOF alarms; final base score times filter with fixed training gate'}
PROTOCOL='''# MRV Daily step2B v1.0
Frozen source: reviewed Daily2A manifest SHA in registration. Verify every parent file, recompute daily labels with Decimal, next-session date alignment and exact shortlist. No new data download, no production mutation.
Target D=max(0,1-low_target/close_previous), severe>=.03, moderate>.012 and<.03, light<=.012. Predict after previous close, no premarket. EOD proxy availability not exact historical16:00 certification.
Two panels: LONG10 removes term9 and term3m, train2007-2018; ALL12 uses all12, train2014-2018. Same complete-feature dates within each panel; missing dates explicitly audited. Calibration2019-2020 and review2021-2022. Compare models only to same-panel same-date B_VIX and B_RV5; not cross-panel ranking. Shortlist was selected using2007-2018, all within training development, not independent validation. Existing years previously studied. No post2022 reads.
M1-M8 have fixed structures/hyperparameters, no review tuning. Train transformations only. M8 uses expanding historical year folds, minimum2 calendar years initial train; entire transform and base model refit inside fold; no contemporaneous or future labels. OOF filter requires>=60 selected rows,>=3 severe and>=10 nonsevere; otherwise BLOCKED with reason. No silent fallback. All fitted models, transformations, thresholds, OOF metadata exported. M5/M6 deterministic bootstrap seed3180125. M2 cumulative probabilities projected to ordered values; severe component used as score. M6 score is quantile, not probability.
Severe decision threshold: exhaustive distinct calibration scores plus below-min boundary, strict score>threshold. Candidate thresholds require non-event moderate false-positive<=.20. Minimize non-event severe misses; then non-event light false positives; then model alarm count; then larger threshold. Include infinite-safe above-max candidate; do not call zero alarms useful. Moderate decision threshold calibrated separately below/equal severe threshold to maximize balanced accuracy for moderate+ vs light, on non-event dates only. Monotone final grades; event override severe. This moderate threshold is secondary diagnostic, not a separately validated probability.
CPI,NFP,scheduled FOMC decision days excluded from BOTH false-positive numerator and denominator; all true severe days retained. Release day only; no minutes, next-day, emergency or holiday shifting. Calendar coverage2019-2022; retrospective proxy with prior-known snapshots unverified. Model-only and combined recalls separately reported. Missed true severe predictions of grade light vs moderate distinguished. Export full3x3 confusion, severity-weighted miss sum (sum actual downside), max missed downside, alarm fraction and longest runs. 'Weighted miss sum' is NOT a portfolio loss estimate.
2B comparison eligibility: calibration false-positive<=20%; review false-positive<=20%; strictly fewer review severe misses than BOTH same-panel B_VIX and B_RV5; no increase in review light false-positive vs B_RV5; complete calibration/review cohort and positive severe/non-event severe denominators. These are preregistered research-comparison rules, not user-promised performance. Zero misses ideal, NOT hard gate. If no eligible model: leading null. Rank within panel by missed severe, light false-positive, alarm count,model id. Never loosen gates after results. Always show all models and Pareto tradeoffs, including useful non-dominant ones. Existing step3 HOLD remains even if research leader found. No automatic step3 execution.
No performance claim before user run. Failure evidence preserved; completed model checkpoints reused only within same run; no resumed mixed inputs. Full invocation starts new isolated timestamp directory.
'''
def transform_fit(X):return [sorted(r[j] for r in X) for j in range(len(X[0]))]
def transform(X,dist):return [[2*((bisect.bisect_left(d,v)+bisect.bisect_right(d,v))/2)/len(d)-1 for d,v in zip(dist,r)] for r in X]
def design(X,spline=False):
 return [[1.]+r+([max(0,v-k) for v in r for k in [-1/3,1/3]] if spline else []) for r in X]
def logfit(X,y,s,lam=.01,spline=False):
 if len(set(y))<2:raise ValueError('SINGLE_CLASS_TRAINING')
 m=s.fit_numeric(design(X,spline),y,'L',lam)
 if not m['converged']:raise ValueError('LOGISTIC_NOT_CONVERGED')
 return m['coef']
def logpred(X,coef,s,spline=False):return [s.sigmoid(sum(a*b for a,b in zip(r,coef))) for r in design(X,spline)]
def tree_fit(X,y,loss,ids,depth,rng,reg=False):
 vals=[loss[i] for i in ids];node={'n':len(ids),'p':(sum(y[i] for i in ids)+.5)/(len(ids)+1),'losses':sorted(vals)}
 if depth==0 or len(ids)<60:return node
 def cost(ix):
  v=[loss[i] if reg else y[i] for i in ix];a=sum(v);return sum(t*t for t in v)-a*a/len(v)
 best=None;parent=cost(ids)
 for j in rng.sample(range(len(X[0])),max(1,int(math.sqrt(len(X[0]))))):
  v=sorted(X[i][j] for i in ids)
  for k in range(1,10):
   cut=v[int((len(v)-1)*k/10)];a=[i for i in ids if X[i][j]<=cut];b=[i for i in ids if X[i][j]>cut]
   if min(len(a),len(b))<30:continue
   score=cost(a)+cost(b)
   if score<parent-1e-12 and (best is None or score<best[0]):best=(score,j,cut,a,b)
 if best is None:return node
 _,j,cut,a,b=best
 return {'j':j,'cut':cut,'left':tree_fit(X,y,loss,a,depth-1,rng,reg),'right':tree_fit(X,y,loss,b,depth-1,rng,reg)}
def leaf(tree,row):
 while 'j' in tree:tree=tree['left'] if row[tree['j']]<=tree['cut'] else tree['right']
 return tree

def fit(kind,X,cls,loss,dates,keys,s,c):
 dist=transform_fit(X);Z=transform(X,dist);y=[int(v=='severe') for v in cls];ym=[int(v!='light') for v in cls];m={'kind':kind,'features':keys,'dist':dist,'n_train':len(X),'train_first':dates[0],'train_last':dates[-1]}
 if kind=='M1':m['coef']=logfit(Z,y,s)
 elif kind=='M2':m['coef_m']=logfit(Z,ym,s);m['coef_s']=logfit(Z,y,s)
 elif kind=='M3':
  ix=[i for i,v in enumerate(ym) if v];m['coef_m']=logfit(Z,ym,s);m['coef_cond']=logfit([Z[i] for i in ix],[y[i] for i in ix],s)
 elif kind=='M4':m['coef']=logfit(Z,y,s,.03,True)
 elif kind in ['M5','M6']:
  rng=random.Random(3180125);m['trees']=[tree_fit(Z,y,loss,[rng.randrange(len(X)) for _ in X],3,rng,kind=='M6') for _ in range(24)]
 elif kind=='M7':
  groups=[['vix','spx_rv5','term9','term3m'],['spx_dd60','spx_dd20','spx_ma20_gap','spx_down20','spx_down10'],['spx_downside20','spx_tail_max5','spx_range']];m['experts']=[]
  for group in groups:
   ix=[j for j,k in enumerate(keys) if k in group]
   if not ix:raise ValueError('EMPTY_EXPERT')
   m['experts'].append({'ix':ix,'coef':logfit([[r[j] for j in ix] for r in Z],y,s)})
 elif kind=='M8':
  records=[];folds=[];years=sorted({d[:4] for d in dates})
  for yr in years[2:]:
   tr=[i for i,d in enumerate(dates) if d[:4]<yr];te=[i for i,d in enumerate(dates) if d[:4]==yr]
   if sum(y[i] for i in tr)<3:continue
   base=fit('M1',[X[i] for i in tr],[cls[i] for i in tr],[loss[i] for i in tr],[dates[i] for i in tr],keys,s,c)
   gate=c.quant(predict(base,[X[i] for i in tr],s,c),.8);scores=predict(base,[X[i] for i in te],s,c)
   for i,p in zip(te,scores):
    if p>gate:records.append({'date':dates[i],'x':X[i]+[p],'y':y[i],'base_p':p})
   folds.append({'test_year':yr,'train_end':dates[tr[-1]],'n_train':len(tr),'n_test':len(te),'gate':gate})
  if len(records)<60 or sum(r['y'] for r in records)<3 or sum(1-r['y'] for r in records)<10:raise ValueError('M8_INSUFFICIENT_OOF_ALARMS')
  m['base']=fit('M1',X,cls,loss,dates,keys,s,c);m['gate']=c.quant(predict(m['base'],X,s,c),.8)
  m['filter_dist']=transform_fit([r['x'] for r in records]);m['filter_coef']=logfit(transform([r['x'] for r in records],m['filter_dist']),[r['y'] for r in records],s)
  m['oof_folds']=folds;m['oof_training']=[{k:v for k,v in r.items() if k!='x'} for r in records]
 else:raise ValueError('UNKNOWN_KIND')
 return m

def predict(m,X,s,c):
 Z=transform(X,m['dist']);k=m['kind']
 if k in ['M1','M4']:return logpred(Z,m['coef'],s,k=='M4')
 if k=='M2':
  a=logpred(Z,m['coef_m'],s);b=logpred(Z,m['coef_s'],s);return [v if v<=u else (u+v)/2 for u,v in zip(a,b)]
 if k=='M3':return [a*b for a,b in zip(logpred(Z,m['coef_m'],s),logpred(Z,m['coef_cond'],s))]
 if k=='M5':return [sum(leaf(t,r)['p'] for t in m['trees'])/len(m['trees']) for r in Z]
 if k=='M6':
  out=[]
  for r in Z:
   weighted=[]
   for t in m['trees']:
    vals=leaf(t,r)['losses'];weighted.extend((v,1/len(vals)/len(m['trees'])) for v in vals)
   acc=0
   for v,w in sorted(weighted):
    acc+=w
    if acc>=.95-1e-12:out.append(v);break
  return out
 if k=='M7':return [sum(v)/len(v) for v in zip(*[logpred([[r[j] for j in e['ix']] for r in Z],e['coef'],s) for e in m['experts']])]
 if k=='M8':
  p=predict(m['base'],X,s,c);q=logpred(transform([r+[v] for r,v in zip(X,p)],m['filter_dist']),m['filter_coef'],s);return [a*b if a>m['gate'] else 0. for a,b in zip(p,q)]
 raise ValueError('UNKNOWN_PREDICT')

def threshold(scores,rows):
 mids=[p for p,r in zip(scores,rows) if not r['events'] and r['class']=='moderate'];sevs=[p for p,r in zip(scores,rows) if not r['events'] and r['class']=='severe'];lights=[p for p,r in zip(scores,rows) if not r['events'] and r['class']=='light']
 if not mids or not sevs or not lights:raise ValueError('CALIBRATION_CLASS_DENOMINATOR_ZERO')
 cand=sorted(set(scores));cand=[cand[0]-max(1,abs(cand[0]))]+cand;grid=[]
 for t in cand:
  fm=sum(v>t for v in mids);miss=sum(v<=t for v in sevs);fl=sum(v>t for v in lights)
  grid.append({'threshold':t,'moderate_false':fm,'moderate_n':len(mids),'non_event_missed':miss,'non_event_severe_n':len(sevs),'light_false':fl,'model_alarm_days':sum(v>t for v in scores),'eligible':fm/len(mids)<=.2})
 best=min([g for g in grid if g['eligible']],key=lambda g:(g['non_event_missed'],g['light_false'],g['model_alarm_days'],-g['threshold']));ts=best['threshold']
 positive=[p for p,r in zip(scores,rows) if not r['events'] and r['class']!='light'];negative=lights
 tm=max((t for t in cand if t<=ts),key=lambda t:((sum(p>t for p in positive)/len(positive)+sum(p<=t for p in negative)/len(negative))/2,t))
 return {'severe':ts,'moderate':tm,'calibration':best},grid

def summarize(scores,rows,th):
 pred=[];conf={(a,b):0 for a in ['light','moderate','severe'] for b in ['light','moderate','severe']};run=longest=0;prev=None
 for p,r in zip(scores,rows):
  raw='severe' if p>th['severe'] else 'moderate' if p>th['moderate'] else 'light';grade='severe' if r['events'] else raw;conf[r['class'],grade]+=1
  run=(run+1 if prev is not None and r['i']==prev+1 else 1) if grade=='severe' else 0;longest=max(longest,run);prev=r['i']
  pred.append(dict(r,score=p,model_grade=raw,final_grade=grade))
 def filt(cls,event=False):return [r for r in pred if r['class']==cls and (event or not r['events'])]
 sev=filt('severe',True);ns=filt('severe');mid=filt('moderate');low=filt('light');miss=[r for r in sev if r['final_grade']!='severe'];fmid=sum(r['final_grade']=='severe' for r in mid);flow=sum(r['final_grade']=='severe' for r in low)
 return {'n':len(rows),'severe_n':len(sev),'missed':len(miss),'severe_recall':1-len(miss)/len(sev) if sev else None,'non_event_severe_n':len(ns),'non_event_missed':sum(r['final_grade']!='severe' for r in ns),'model_only_missed':sum(r['model_grade']!='severe' for r in sev),'missed_as_light':sum(r['final_grade']=='light' for r in miss),'missed_as_moderate':sum(r['final_grade']=='moderate' for r in miss),'max_missed_loss':max([r['loss'] for r in miss],default=0),'sum_missed_loss':sum(r['loss'] for r in miss),'moderate_n':len(mid),'moderate_false':fmid,'moderate_false_rate':fmid/len(mid) if mid else None,'light_n':len(low),'light_false':flow,'light_false_rate':flow/len(low) if low else None,'alarm_days':sum(r['final_grade']=='severe' for r in pred),'longest_alarm_run':longest},pred,[{'actual':a,'predicted':b,'n':v} for (a,b),v in conf.items()]

def load(root,out,c,d):
 base=c.safe(root,'reports/step2A/MRV-DAILY-01');matches=[]
 for p in sorted(base.glob('*/manifest.json')):
  c.safe(root,str(p.relative_to(root)))
  if c.sha(p)==PARENT_HASH:matches.append(p.parent)
 if not matches:raise ValueError('REVIEWED_DAILY_2A_NOT_FOUND')
 parent=matches[0];manifest=json.loads((parent/'manifest.json').read_text())
 for rel,h in manifest.items():
  if c.sha(c.safe(parent,rel))!=h:raise ValueError('PARENT_HASH_MISMATCH:'+rel)
 result=json.loads((parent/'result.json').read_text())
 if result['state']!='COMPLETE' or result['factor_count']!=50:raise ValueError('PARENT_NOT_COMPLETE')
 keys=json.loads((parent/'shortlist.json').read_text())['selected'];feat={int(r['i']):r for r in c.rows(parent/'features.csv')};calendar=[r['date'] for r in c.rows(parent/'inputs/calendar.csv')] if (parent/'inputs/calendar.csv').exists() else None
 # Exact indexed trading calendar supplies next-session audit; never infer weekdays.
 index=json.loads(c.safe(root,'config/data-index.json').read_text());item=index['files']['contracts/historical-session-calendar.csv'];cp=c.safe(root,item['path'])
 if c.sha(cp)!=item['sha256']:raise ValueError('CALENDAR_INDEX_HASH')
 dates=[r['date'] for r in c.rows(cp) if '2006-01-01'<=r['date']<='2022-12-31']
 rows=[]
 for r in c.rows(parent/'labels-daily.csv'):
  i=int(r['i']);loss,cls=d.label(r['previous_close'],r['target_low'])
  if cls!=r['class'] or abs(loss-float(r['loss']))>1e-12 or dates[i]!=r['target_date'] or dates[i-1]!=r['feature_date']:raise ValueError('DAILY_LABEL_ALIGNMENT')
  raw=feat.get(i,{});x={k:float(raw[k]) if raw.get(k) not in [None,'','None'] else None for k in keys}
  if raw and (raw['target_date']!=dates[i] or raw['feature_date']!=dates[i-1]):raise ValueError('FACTOR_ALIGNMENT')
  if any(v is not None and not math.isfinite(v) for v in x.values()):raise ValueError('NONFINITE_INPUT')
  ev=json.loads(r['event_status']) if r['event_status']!='UNKNOWN_PRE2019' else None
  rows.append({'i':i,'date':dates[i],'feature_date':dates[i-1],'loss':loss,'class':cls,'events':ev,'x':x})
 for rel in ['features.csv','labels-daily.csv','shortlist.json','calendar.json','source-provenance.json']:
  c.write(out/'inputs'/rel,(parent/rel).read_bytes())
 c.dump(out/'input-audit.json',{'parent':str(parent.relative_to(root)),'manifest_sha256':PARENT_HASH,'verified_files':len(manifest),'calendar_sha256':item['sha256']})
 return keys,rows

def run(root,out,c,d,s,preflight=False):
 c.write(out/'protocol.md',PROTOCOL.encode());c.dump(out/'registration.json',{'version':VERSION,'parent_manifest':PARENT_HASH,'specs':SPECS,'panels':['LONG10','ALL12'],'model_count':16,'baseline_count':4,'lambda':.01,'fit_before':'2019-01-01','calibration':'2019-2020','review':'2021-2022','zero_miss_is_hard_gate':False,'moderate_false_cap':.2,'step3':'HOLD'})
 c.dump(out/'tests.json',selftest(c,d,s));keys,rows=load(root,out,c,d);panels={'LONG10':[k for k in keys if k not in ['term9','term3m']],'ALL12':keys};cohorts={};audit=[]
 for panel,ks in panels.items():
  start='2007' if panel=='LONG10' else '2014';parts={}
  for name,lo,hi in [('train',start,'2018-12-31'),('calibration','2019','2020-12-31'),('review','2021','2022-12-31')]:
   eligible=[r for r in rows if lo<=r['date']<=hi];valid=[r for r in eligible if all(r['x'][k] is not None for k in ks)]
   for r in eligible:audit.append({'panel':panel,'period':name,'date':r['date'],'class':r['class'],'included':all(r['x'][k] is not None for k in ks),'missing_factors':[k for k in ks if r['x'][k] is None]})
   if len(valid)<100 or not any(r['class']=='severe' for r in valid):raise ValueError('INSUFFICIENT_PANEL_DATA:'+panel+name)
   parts[name]=valid
  parts['complete']=all(a['included'] for a in audit if a['panel']==panel and a['period']!='train');cohorts[panel]=parts
 c.csvwrite(out/'cohort-audit.csv',audit);c.dump(out/'sample-counts.json',{p:{k:{'n':len(v),'severe':sum(r['class']=='severe' for r in v),'first':v[0]['date'],'last':v[-1]['date']} for k,v in parts.items() if k!='complete'} for p,parts in cohorts.items()})
 c.dump(out/'runtime.json',{'python':sys.version,'platform':platform.platform(),'standard_library_only':True,'network':False,'independent_validation':False})
 if preflight:c.dump(out/'result.json',{'state':'PREFLIGHT_PASS','models_fitted':0,'step3':'HOLD'});return
 metrics=[];predictions=[];confusions=[];status=[];allgrids=[]
 for panel,ks in panels.items():
  parts=cohorts[panel];tr=parts['train'];ca=parts['calibration'];te=parts['review'];X=lambda rr:[[r['x'][k] for k in ks] for r in rr]
  for kind in ['B_VIX','B_RV5']+MODELS:
   ident=panel+'_'+kind;print('FITTING='+ident,flush=True)
   try:
    if kind.startswith('B_'):
     key='vix' if kind=='B_VIX' else 'spx_rv5';model={'kind':kind,'feature':key};pc=[r['x'][key] for r in ca];pt=[r['x'][key] for r in te]
    else:
     model=fit(kind,X(tr),[r['class'] for r in tr],[r['loss'] for r in tr],[r['date'] for r in tr],ks,s,c);pc=predict(model,X(ca),s,c);pt=predict(model,X(te),s,c)
    if not all(math.isfinite(v) for v in pc+pt):raise ValueError('NONFINITE_SCORE')
    th,grid=threshold(pc,ca);allgrids.extend(dict(panel=panel,model=kind,**g) for g in grid);c.dump(out/'models'/(ident+'.json'),{'model':model,'thresholds':th})
    for period,rs,ps in [('calibration',ca,pc),('review',te,pt)]:
     mm,pp,cc=summarize(ps,rs,th);metrics.append(dict(panel=panel,model=kind,period=period,**mm))
     predictions.extend(dict(panel=panel,model=kind,period=period,**{k:v for k,v in r.items() if k!='x'}) for r in pp);confusions.extend(dict(panel=panel,model=kind,period=period,**r) for r in cc)
     for yr in sorted({r['date'][:4] for r in rs}):
      ix=[i for i,r in enumerate(rs) if r['date'].startswith(yr)];mm,_,_=summarize([ps[i] for i in ix],[rs[i] for i in ix],th);metrics.append(dict(panel=panel,model=kind,period=period+'_'+yr,**mm))
    status.append({'panel':panel,'model':kind,'state':'COMPLETE'})
   except (ValueError,ArithmeticError) as ex:
    status.append({'panel':panel,'model':kind,'state':'BLOCKED','reason':str(ex)});print('MODEL_BLOCKED='+ident+':'+str(ex),flush=True)
 c.csvwrite(out/'metrics.csv',metrics);c.csvwrite(out/'predictions.csv',predictions);c.csvwrite(out/'confusion.csv',confusions);c.csvwrite(out/'calibration-grid.csv',allgrids);c.csvwrite(out/'model-status.csv',status)
 assessments=[];leaders={};pareto=[]
 for panel in panels:
  mm={r['model']:r for r in metrics if r['panel']==panel and r['period']=='review'};base=mm.get('B_RV5');vix=mm.get('B_VIX');eligible=[]
  for name,r in mm.items():
   vec=(r['missed'],r['moderate_false_rate'],r['light_false_rate'],r['alarm_days']);dom=[]
   if None not in vec:
    for other,t in mm.items():
     vv=(t['missed'],t['moderate_false_rate'],t['light_false_rate'],t['alarm_days'])
     if other!=name and None not in vv and all(a<=b for a,b in zip(vv,vec)) and any(a<b for a,b in zip(vv,vec)):dom.append(other)
   pareto.append({'panel':panel,'model':name,'dominated_by':dom,'on_frontier':not dom})
  for kind in MODELS:
   r=mm.get(kind)
   if not r:continue
   checks={'moderate_false_le20':r['moderate_false_rate'] is not None and r['moderate_false_rate']<=.2,'fewer_misses_than_both_baselines':bool(base and vix and r['missed']<min(base['missed'],vix['missed'])),'light_false_no_worse_than_RV5':bool(base and r['light_false_rate'] is not None and r['light_false_rate']<=base['light_false_rate']),'complete_cohort':cohorts[panel]['complete'],'non_event_severe_exists':r['non_event_severe_n']>0}
   ok=all(checks.values());assessments.append({'panel':panel,'model':kind,'checks':checks,'qualified_research':ok,'zero_misses_observed':r['missed']==0})
   if ok:eligible.append(kind)
  leaders[panel]=min(eligible,key=lambda k:(mm[k]['missed'],mm[k]['light_false_rate'],mm[k]['alarm_days'],k)) if eligible else None
 c.csvwrite(out/'pareto.csv',pareto);c.dump(out/'assessment.json',assessments);c.dump(out/'result.json',{'state':'COMPLETE','research_leaders_by_panel':leaders,'risk_acceptance':'HOLD','step3':'PREVIOUS_HOLD_UNCHANGED','independent_validation':False,'calendar_prior_known_verified':False,'blocked_models':[r for r in status if r['state']=='BLOCKED']})
 lines=['# MRV Daily step2B','', '研究领先（分样本组）：'+json.dumps(leaders),'风险有效性HOLD；不自动进入step3或实盘。','', '方案|样本组|严重漏报|非发布日中等误报|非发布日轻度误报|严重报警日','---|---|---:|---:|---:|---:']
 for r in metrics:
  if r['period']=='review':lines.append('%s|%s|%d/%d|%s|%s|%d/%d'%(r['model'],r['panel'],r['missed'],r['severe_n'],str(r['moderate_false_rate']),str(r['light_false_rate']),r['alarm_days'],r['n']))
 lines+=['','M1-M8含义见registration.json；BLOCKED原因见model-status.csv。','比较须同组同日期；LONG10长历史训练，ALL12含全部期限结构但训练严重样本较少。','零漏报是理想目标，不是硬淘汰条件。20%误报约束在校准选择，复查仍需检查，不保证样本外保持。','累计漏报跌幅不是交易损失。全部3级混淆矩阵与严重日预测均已输出。','历史已被反复研究，日历事前版本及精确收盘可得时点尚未认证；研究领先不等于可部署。','请回传evidence.zip。']
 c.write(out/'REPORT.md','\n'.join(lines).encode())

def selftest(c,d,s):
 checks=[]
 def ck(n,v):
  if not v:raise AssertionError(n)
  checks.append(n)
 X=[[float(i%17),math.sin(i)] for i in range(180)];cls=['severe' if i%7==0 else 'moderate' if i%3==0 else 'light' for i in range(180)];loss=[.04 if v=='severe' else .02 if v=='moderate' else .005 for v in cls];dates=['2014-%02d-%02d'%(1+i//28,1+i%28) for i in range(180)]
 for k in ['M1','M2','M3','M4','M5','M6']:
  m=fit(k,X,cls,loss,dates,['a','b'],s,c);p=predict(m,X[:5],s,c);ck(k+'_finite',len(p)==5 and all(math.isfinite(v) for v in p));ck(k+'_serialization',p==predict(json.loads(json.dumps(m)),X[:5],s,c))
 dist=transform_fit(X[:50]);before=transform(X[:10],dist);X[-1]=[999,999];ck('transform_train_only',before==transform(X[:10],dist))
 rows=[{'i':i,'date':str(i),'class':v,'events':['CPI'] if i==0 else [],'loss':loss[i]} for i,v in enumerate(cls)];scores=[i/180 for i in range(180)];th,g=threshold(scores,rows);ck('calibration_cap',th['calibration']['moderate_false']/th['calibration']['moderate_n']<=.2);ck('ordered_threshold',th['moderate']<=th['severe']);mm,pp,cf=summarize(scores,rows,th);ck('event_override',pp[0]['final_grade']=='severe');ck('event_kept_severe_denominator',mm['severe_n']==cls.count('severe'));ck('no_next_day_override',pp[1]['final_grade']==pp[1]['model_grade']);ck('confusion_total',sum(r['n'] for r in cf)==len(rows));ck('severity_miss_breakdown',mm['missed']==mm['missed_as_light']+mm['missed_as_moderate'])
 exX=[r+[math.cos(i)] for i,r in enumerate(X)];ex=fit('M7',exX,cls,loss,dates,['vix','spx_dd20','spx_range'],s,c);ep=predict(ex,exX[:5],s,c);ck('M7_three_experts',len(ex['experts'])==3);ck('M7_serialization',ep==predict(json.loads(json.dumps(ex)),exX[:5],s,c))
 blocked=False
 try:fit('M8',X,cls,loss,dates,['a','b'],s,c)
 except ValueError as err:blocked=str(err)=='M8_INSUFFICIENT_OOF_ALARMS'
 ck('M8_small_sample_blocks',blocked)
 tied=[.5]*len(rows);tt,_=threshold(tied,rows);mt,_,_=summarize(tied,rows,tt);ck('strict_tie_threshold',tt['severe']==.5 and mt['moderate_false']==0)
 newrows=[dict(r,events=['NFP'] if r['class']=='moderate' else r['events']) for r in rows];em,_,_=summarize(scores,newrows,th);ck('events_excluded_denominator',em['moderate_n']==0 and em['moderate_false_rate'] is None)
 ck('thresholds_no_review_input',threshold(scores,rows)[0]==th)
 return {'status':'PASS','count':len(checks),'checks':checks}
