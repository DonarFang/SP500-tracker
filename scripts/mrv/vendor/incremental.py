import argparse,datetime as dt,hashlib,io,json,math,platform,statistics as st,sys,traceback,types,uuid,zipfile
from pathlib import Path
VERSION='MRV-step-2B-Incremental-v1.0'
PARENT='ba4ed282efd8be68a0e274bf42be26c9dc042f50323029c7c525f20f31e2907c'
LAMBDA=.01
SPECS={
 'C7':('ALL12_M7',[]),
 'I7R':('ALL12_M7',['stress_vix_cooling','stress_rv_cooling']),
 'I7RT':('ALL12_M7',['stress_vix_cooling','stress_rv_cooling','tail_spx_downside20']),
 'I7RTE':('ALL12_M7',['stress_vix_cooling','stress_rv_cooling','tail_spx_downside20','after_nfp1']),
 'C6':('LONG10_M6',[]),
 'I6V':('LONG10_M6',['vix_delta5']),
 'I6VT':('LONG10_M6',['vix_delta5','tail_spx_downside20']),
 'I6VTE':('LONG10_M6',['vix_delta5','tail_spx_downside20','after_nfp1'])}
CANDIDATES=[k for k in SPECS if k.startswith('I')]
PROTOCOL="""# MRV-step-2B 增量组合验证 v1.0
6增量候选+2校准对照+2冻结基线；不增加网格、不改已冻结M7/M6。
I7R：M7分数+stress_vix_cooling+stress_rv_cooling。
I7RT：I7R+tail_spx_downside20。
I7RTE：I7RT+after_nfp1。
I6V：M6分数+vix_delta5。
I6VT：I6V+tail_spx_downside20。
I6VTE：I6VT+after_nfp1。
C7/C6：同样的拟合和校准流程，仅输入对应基线分数。F7/F6：原冻结分数和等级。
所有增量因子完全继承审核的2A定义和2014—2018变换参数；不从评估年学习变换。
数学模型：p=sigmoid(beta0+sum beta_j*z_j)，最小化平均二元交叉熵+0.01/2*sum(beta_j^2)，截距不惩罚，无类别重加权。y=严重日。训练包含所有可用日，包括发布日；发布日仍另行强制覆盖。
M7基础输入为clip到[1e-8,1-1e-8]后的logit(score)（原分数并非经验证的概率，仅作单调输入变换）；M6基础输入为原条件95%分位值。连续回归输入用训练中位数/IQR做asinh变换；若IQR为0用训练总体标准差，若仍为0则列为训练常量并固定变换为0。after_nfp1保留0/1。全为训练期参数。
各年一次冻结：测试2021，训练2019、校准2020；测试2022，训练2019—20、校准2021；依次扩展，测试2025训练2019—23、校准2024。校准年不参与系数拟合，测试年不参与任何参数或阈值选择。
每个校准集按非发布中等日分数选择满足<=20%误报的最低阈值；严格score>threshold才严重，完整处理并列值。校准中等日少于10则失败，不猜阈值。没有非发布严重日时照常校准，但明确披露无法校准该年严重召回；不把0/0报为100%。
该设计不保证未来或每年误报<=20%；全部如实报告。原基线与对应C对照必须在相同测试日期比较。
训练缺失行排除并计数；校准/测试新增因子不完整则停止，不以0代缺失、不静默缩小测试分母。
新回归可以升级或降级原严重信号：分别报告补回与新增漏报。非严重日等级继承原轻度/中等；原严重被降级后标中等。只拟合严重端点，不声称中等/轻度阈值已重新优化。
标签：max(0,1-目标日最低/前一交易日收盘)；严重>=3%，中等>1.2%且<3%，轻度<=1.2%。不使用盘前数据。CPI/NFP/预定FOMC当日强制严重；误报分子分母完整排除发布日，严重日全部保留。
after_nfp1仅为回归因子，不扩展强制严重日历。外部信用/汇率/政策公告未通过历史可得性审计，本轮不用。
输出2021—2025逐年、2021—22、2023—25、整体指标；2019—20仅作拟合/校准，不包装成增量模型验证。旧2A及step3已看过2021—25；这是历史探索回放，不是新独立OOS。
对每候选同时比较冻结基线与C对照，输出严重漏报、中等/轻度误报、预警总量/连续天数、混淆矩阵、AUC/Brier、分数与模型参数、训练/校准清单及哈希。Brier和概率校准仅描述，不等于已认证概率。
不自动生成交易许可、不设未经同意的轻度误报硬门槛、不自动部署。研究候选表报告整体20%目标和逐年超标，输出Pareto而不是强行选冠军；risk始终HOLD。
所有输出限UEIS-MRV/reports/step2B/MRV-INCREMENTAL-01的新目录。原2A、M7/M6、step3保持不变。离线Python3.9标准库。
"""
def sha(b):return hashlib.sha256(b).hexdigest()
def sigmoid(x):
 if x>=0:return 1/(1+math.exp(-x))
 a=math.exp(x);return a/(1+a)
def solve(a,b):
 n=len(b);a=[list(r)+[v] for r,v in zip(a,b)]
 for j in range(n):
  k=max(range(j,n),key=lambda k:abs(a[k][j]))
  if abs(a[k][j])<1e-14:raise ValueError('SINGULAR_HESSIAN')
  a[j],a[k]=a[k],a[j];v=a[j][j]
  a[j]=[x/v for x in a[j]]
  for i in range(n):
   if i==j:continue
   v=a[i][j]
   for k in range(j,n+1):a[i][k]-=v*a[j][k]
 return [r[-1] for r in a]
def softplus(x):return max(0,x)+math.log1p(math.exp(-abs(x)))
def objective(X,y,b):
 return st.mean(softplus(sum(x*v for x,v in zip(r,b)))-yy*sum(x*v for x,v in zip(r,b)) for r,yy in zip(X,y))+LAMBDA/2*sum(v*v for v in b[1:])
def fit(X,y):
 if not X or len(set(y))!=2:raise ValueError('TRAINING_REQUIRES_BOTH_CLASSES')
 X=[[1.]+r for r in X];n=len(X);q=len(X[0]);pi=st.mean(y);b=[math.log(pi/(1-pi))]+[0.]*(q-1)
 for iteration in range(100):
  probs=[sigmoid(sum(x*v for x,v in zip(r,b))) for r in X]
  g=[sum((p-yy)*r[j] for r,p,yy in zip(X,probs,y))/n+(LAMBDA*b[j] if j else 0) for j in range(q)]
  if max(map(abs,g))<1e-8:return {'coef':b,'iterations':iteration,'max_gradient':max(map(abs,g)),'converged':True}
  h=[[sum(p*(1-p)*r[j]*r[k] for r,p in zip(X,probs))/n+(LAMBDA if j==k and j else 0) for k in range(q)] for j in range(q)]
  delta=solve(h,g);old=objective(X,y,b);step=1.
  for _ in range(30):
   trial=[v-step*d for v,d in zip(b,delta)]
   if objective(X,y,trial)<=old+1e-14:b=trial;break
   step*=.5
  else:raise ValueError('LINE_SEARCH_FAILED')
 raise ValueError('FIT_NOT_CONVERGED')
def predict(X,model):return [sigmoid(model['coef'][0]+sum(x*b for x,b in zip(r,model['coef'][1:]))) for r in X]
def scale_fit(X,keys):
 params=[]
 for j,k in enumerate(keys):
  values=sorted(r[j] for r in X);n=len(values)
  if k=='after_nfp1':params.append({'kind':'binary'});continue
  med=st.median(values);scale=values[math.ceil(.75*n)-1]-values[math.ceil(.25*n)-1]
  if scale<1e-12:scale=st.pstdev(values)
  params.append({'kind':'constant' if scale<1e-12 else 'asinh','median':med,'scale':scale})
 return params
def transform(X,params):
 return [[v if p['kind']=='binary' else 0. if p['kind']=='constant' else math.asinh((v-p['median'])/p['scale']) for v,p in zip(r,params)] for r in X]
def select_threshold(scores,labels):
 mids=sorted([s for s,r in zip(scores,labels) if r['class']=='moderate' and not r['events']],reverse=True)
 if len(mids)<10:raise ValueError('CALIBRATION_MODERATE_N_LT10')
 t=mids[len(mids)//5]
 if sum(s>t for s in mids)>len(mids)//5:raise AssertionError('THRESHOLD_CAP')
 return t
def raw_input(base,score,vals,keys):
 if base=='ALL12_M7':
  p=min(1-1e-8,max(1e-8,score));score=math.log(p/(1-p))
 return [score]+[vals[k] for k in keys]
def grade(severe,base_grade):return 'severe' if severe else ('light' if base_grade=='light' else 'moderate')
def parts(year,dates):
 return ([d for d in dates if '2019'<=d<str(year-1)],[d for d in dates if str(year-1)<=d<str(year)],[d for d in dates if str(year)<=d<str(year+1)])
def aux(package):
 mod=types.ModuleType('incremental2a')
 exec(compile(package['parent_runner.py'],'reviewed_2a_runner.py','exec'),mod.__dict__)
 return mod
def load(package,a):
 z=a.archive(package['parent-2A.zip'],PARENT)
 if z.read('implementation/runner.py')!=package['parent_runner.py']:raise ValueError('REVIEWED_LOADER_CHANGED')
 status=json.loads(z.read('result.json'))
 if status['engineering']!='PASS' or status['state']!='COMPLETE_REVIEW_REQUIRED':raise ValueError('2A_NOT_COMPLETE')
 fs,labs,models,preds,repro=a.load({'parent-2B.zip':z.read('inputs/parent-2B.zip'),'parent-3.zip':z.read('inputs/parent-3.zip')})
 factors,params=a.make_factors(fs,labs)
 saved=a.csvrows(z.read('incremental-features.csv'))
 for r in saved:
  d=r['date']
  for k in a.FACTORS:
   v=None if r[k]=='' else float(r[k])
   if (v is None)!=(factors[d][k] is None) or (v is not None and abs(v-factors[d][k])>1e-12):raise ValueError('2A_FACTOR_REPRODUCTION:'+d+':'+k)
 if len(saved)!=len(factors):raise ValueError('2A_FACTOR_COHORT')
 return fs,labs,models,preds,factors,params,repro
def local_parent(root,a):
 matches=[];base=a.within(root,'reports/step2A/MRV-INCREMENTAL-01')
 if base.exists():
  for p in sorted(base.glob('*/manifest.json')):
   a.within(root,str(p.relative_to(root)))
   if sha(p.read_bytes())!=PARENT:continue
   for rel,h in json.loads(p.read_text()).items():
    q=a.within(root,str((p.parent/rel).relative_to(root)))
    if not q.is_file() or sha(q.read_bytes())!=h:raise ValueError('LOCAL_2A_CHANGED:'+rel)
   matches.append(str(p.parent.relative_to(root)))
 return {'matches':matches,'source':'bundled verified reviewed 2A snapshot','status':'MATCHED' if matches else 'LOCAL_NOT_FOUND_BUNDLED_SNAPSHOT'}
def metrics_for(rows,labs,a):
 ds=sorted(r['date'] for r in rows);lookup={r['date']:r for r in rows}
 result=a.measure(ds,labs,lambda d:lookup[d]['model_grade']=='severe')
 non=[r for r in rows if not labs[r['date']]['events']]
 result['non_event_auc']=a.auc([r['score'] for r in non],[int(labs[r['date']]['class']=='severe') for r in non])
 result['non_event_brier']=st.mean((r['score']-int(labs[r['date']]['class']=='severe'))**2 for r in non) if non and rows[0]['kind']!='FROZEN' else None
 return result
def run_study(labs,preds,factors,out,a):
 dates=sorted(preds['ALL12_M7']);allpred=[];foldaudit=[];calrows=[];artifacts=[]
 for year in range(2021,2026):
  tr,ca,te=parts(year,dates)
  if not tr or not ca or not te or not max(tr)<min(ca) or not max(ca)<min(te):raise ValueError('TEMPORAL_SPLIT')
  for k,(base,extra) in SPECS.items():
   print('FOLD='+str(year)+' MODEL='+k,flush=True)
   keys=['base_score']+extra
   train=[d for d in tr if all(factors[d].get(x) is not None for x in extra)]
   for d in ca+te:
    if any(factors[d].get(x) is None for x in extra):raise ValueError('EVALUATION_FEATURE_MISSING:'+k+':'+d)
   def matrix(ds):return [raw_input(base,preds[base][d]['score'],factors[d],extra) for d in ds]
   x=matrix(train);scaler=scale_fit(x,keys);xx=transform(x,scaler);y=[int(labs[d]['class']=='severe') for d in train]
   model=fit(xx,y);cs=predict(transform(matrix(ca),scaler),model);th=select_threshold(cs,[labs[d] for d in ca])
   cm=a.measure(ca,labs,lambda d:cs[ca.index(d)]>th)
   artifact={'id':k,'base':base,'test_year':year,'features':keys,'scaler':scaler,'model':model,'severe_threshold':th,'lambda':LAMBDA,'train_dates':train,'calibration_dates':ca,'train_excluded_dates':sorted(set(tr)-set(train)),'train_severe_n':sum(y),'calibration_metrics':cm,'calibration_has_non_event_severe':cm['non_event_severe_n']>0,'model_kind':'regularized_logistic','test_used_in_fit':False}
   path=out/'models'/str(year)/(k+'.json');path.parent.mkdir(parents=True,exist_ok=True);a.js(path,artifact)
   locked=sha(path.read_bytes());artifacts.append({'path':str(path.relative_to(out)),'sha256':locked})
   # Test inference begins only after fitted parameters and threshold are serialized.
   ps=predict(transform(matrix(te),scaler),model)
   for d,s in zip(te,ps):
    bg=preds[base][d];g=grade(s>th,bg['model_grade']);final='severe' if labs[d]['events'] else g
    allpred.append({'id':k,'base':base,'kind':'CALIBRATION_CONTROL' if k.startswith('C') else 'CANDIDATE','fold':year,**labs[d],'score':s,'threshold':th,'model_grade':g,'final_grade':final,'base_score':bg['score'],'base_grade':bg['model_grade'],'base_final':bg['final_grade'],'parameter_sha256':locked})
   if sha(path.read_bytes())!=locked:raise ValueError('MODEL_CHANGED_AFTER_TEST')
   foldaudit.append({'id':k,'test_year':year,'train_first':train[0],'train_last':train[-1],'train_n':len(train),'train_severe_n':sum(y),'train_missing_n':len(tr)-len(train),'calibration_first':ca[0],'calibration_last':ca[-1],'test_first':te[0],'test_last':te[-1],'test_n':len(te),'fit_iterations':model['iterations'],'fit_max_gradient':model['max_gradient'],'threshold':th,'calibration_has_non_event_severe':cm['non_event_severe_n']>0})
   calrows.append({'id':k,'test_year':year,**cm})
  for ident,base in [('F7','ALL12_M7'),('F6','LONG10_M6')]:
   for d in te:
    pp=preds[base][d];allpred.append({'id':ident,'base':base,'kind':'FROZEN','fold':year,**labs[d],**pp,'base_score':pp['score'],'base_grade':pp['model_grade'],'base_final':pp['final_grade']})
 a.writecsv(out/'predictions.csv',allpred);a.writecsv(out/'fold-audit.csv',foldaudit);a.writecsv(out/'calibration-metrics.csv',calrows);a.js(out/'model-hashes.json',artifacts)
 periods=[(str(y),str(y),str(y)+'-12-31') for y in range(2021,2026)]+[('2021-2022','2021','2022-12-31'),('2023-2025','2023','2025-12-31'),('2021-2025','2021','2025-12-31')]
 metrics=[];conf=[];comparisons=[];misses=[]
 lookup={(r['id'],r['date']):r for r in allpred}
 ids=['F7','C7','I7R','I7RT','I7RTE','F6','C6','I6V','I6VT','I6VTE']
 for ident in ids:
  rr=[r for r in allpred if r['id']==ident]
  for period,lo,hi in periods:
   sub=[r for r in rr if lo<=r['date']<=hi]
   metrics.append({'id':ident,'period':period,**metrics_for(sub,labs,a)})
   for mode in ['model_only','combined','event_only']:
    for actual in ['light','moderate','severe']:
     for predicted in ['light','moderate','severe']:
      def pg(r):return r['model_grade'] if mode=='model_only' else r['final_grade'] if mode=='combined' else 'severe' if r['events'] else 'light'
      conf.append({'id':ident,'period':period,'mode':mode,'actual':actual,'predicted':predicted,'n':sum(r['class']==actual and pg(r)==predicted for r in sub)})
  misses.extend(r for r in rr if r['class']=='severe' and r['final_grade']!='severe')
  if ident in CANDIDATES:
   for comparator in (['F7','C7'] if ident.startswith('I7') else ['F6','C6']):
    for period,lo,hi in periods:
     sub=[r for r in rr if lo<=r['date']<=hi]
     cmp=[lookup[comparator,r['date']] for r in sub]
     cm=metrics_for(cmp,labs,a);mm=metrics_for(sub,labs,a)
     comparisons.append({'id':ident,'comparator':comparator,'period':period,'same_dates':True,'rescued_severe':sum(r['class']=='severe' and r['final_grade']=='severe' and b['final_grade']!='severe' for r,b in zip(sub,cmp)),'newly_missed_severe':sum(r['class']=='severe' and r['final_grade']!='severe' and b['final_grade']=='severe' for r,b in zip(sub,cmp)),'net_misses_delta':mm['missed']-cm['missed'],'moderate_false_delta':mm['moderate_false']-cm['moderate_false'],'light_false_delta':mm['light_false']-cm['light_false'],'alarm_days_delta':mm['alarm_days']-cm['alarm_days']})
 summary=[]
 overall={r['id']:r for r in metrics if r['period']=='2021-2025'}
 for ident in CANDIDATES:
  r=overall[ident];base='F7' if ident.startswith('I7') else 'F6';control='C7' if ident.startswith('I7') else 'C6'
  annual=[m for m in metrics if m['id']==ident and len(m['period'])==4]
  vec=lambda m:(m['missed'],m['moderate_false'],m['light_false'],m['alarm_days'])
  v=vec(r);dom=[k for k,m in overall.items() if k!=ident and all(x<=y for x,y in zip(vec(m),v)) and any(x<y for x,y in zip(vec(m),v))]
  summary.append({'id':ident,'overall_mid_le20':r['moderate_false_rate']<=.2,'fewer_misses_than_frozen':r['missed']<overall[base]['missed'],'fewer_misses_than_calibration_control':r['missed']<overall[control]['missed'],'years_mid_over20':[m['period'] for m in annual if m['moderate_false_rate'] is not None and m['moderate_false_rate']>.2],'dominated_by':dom,'leading_model':False,'status':'REVIEW_REQUIRED','not_independent_validation':True})
 a.writecsv(out/'metrics.csv',metrics);a.writecsv(out/'confusion.csv',conf);a.writecsv(out/'paired-comparisons.csv',comparisons);a.writecsv(out/'missed-severe-days.csv',misses);a.writecsv(out/'candidate-review.csv',summary)
 return metrics,summary
def selftest(a):
 checks=[]
 def ck(n,v):
  if not v:raise AssertionError(n)
  checks.append(n)
 X=[[-2.],[-1.],[-.5],[.5],[1.],[2.]];y=[0,0,0,1,1,1];model=fit(X,y);p=predict(X,model)
 ck('logit_converged',model['converged'] and model['max_gradient']<1e-8)
 ck('logit_order',p==sorted(p) and p[0]<.5<p[-1])
 ck('linear_solver',max(abs(x-y) for x,y in zip(solve([[2.,1.],[1.,3.]],[1.,2.]),[.2,.6]))<1e-12)
 ck('sigmoid_extremes',sigmoid(1000)==1 and sigmoid(-1000)==0)
 ck('finite_softplus',math.isfinite(softplus(1000)))
 try:fit(X,[0]*6);ok=False
 except ValueError:ok=True
 ck('single_class_refused',ok)
 par=scale_fit([[1.,0],[1.,1],[1.,0]],['base_score','after_nfp1']);tx=transform([[100,1]],par)
 ck('constant_column_safe',tx==[[0.,1]])
 par=scale_fit([[x] for x in [0,1,2,3,4]],['x']);ck('tail_not_clipped',transform([[100]],par)[0][0]>transform([[10]],par)[0][0])
 labels=[{'class':'moderate','events':[]} for _ in range(10)]
 th=select_threshold(list(range(10)),labels);ck('cap_and_strict_boundary',th==7 and sum(i>th for i in range(10))==2)
 th=select_threshold([1]*10,labels);ck('ties_safe',th==1 and not 1>th)
 try:select_threshold([1]*9,labels[:9]);ok=False
 except ValueError:ok=True
 ck('small_calibration_refused',ok)
 ev=[{'class':'moderate','events':['CPI']}]*5
 ck('event_excluded_calibration',select_threshold(list(range(10))+[100]*5,labels+ev)==7)
 dd=['2019-01-02','2020-01-02','2021-01-02','2022-01-03']
 tr,ca,te=parts(2021,dd);ck('temporal_partition',tr==dd[:1] and ca==dd[1:2] and te==dd[2:3])
 ck('nonsevere_inheritance',grade(False,'severe')=='moderate' and grade(False,'light')=='light')
 ck('scope_six_candidates',len(CANDIDATES)==6 and len(SPECS)==8)
 return {'status':'PASS','count':len(checks),'checks':checks}
def preflight_folds(labs,preds,factors):
 dates=sorted(preds['ALL12_M7']);rr=[]
 for year in range(2021,2026):
  tr,ca,te=parts(year,dates)
  for k,(base,extras) in SPECS.items():
   train=[d for d in tr if all(factors[d].get(x) is not None for x in extras)]
   if len(set(labs[d]['class']=='severe' for d in train))!=2:raise ValueError('TRAIN_CLASS_PREFLIGHT')
   if any(factors[d].get(x) is None for d in ca+te for x in extras):raise ValueError('FEATURE_PREFLIGHT')
   mid=sum(labs[d]['class']=='moderate' and not labs[d]['events'] for d in ca)
   if mid<10:raise ValueError('CALIBRATION_PREFLIGHT')
   rr.append({'id':k,'test_year':year,'train_n':len(train),'calibration_n':len(ca),'test_n':len(te),'calibration_non_event_moderate_n':mid,'train_severe_n':sum(labs[d]['class']=='severe' for d in train)})
 return rr
def main(package,source):
 ap=argparse.ArgumentParser();ap.add_argument('--root',default=str(Path.home()/'UEIS-MRV'));ap.add_argument('--self-test',action='store_true');ap.add_argument('--preflight',action='store_true');args=ap.parse_args()
 a=aux(package);tests={'current':selftest(a),'inherited_2A':a.selftest()}
 if args.self_test:print(json.dumps(tests));return
 raw=Path(args.root).expanduser()
 if raw.is_symlink():raise ValueError('MRV_ROOT_SYMLINK_REFUSED')
 root=raw.resolve()
 if not root.is_dir() or root.name!='UEIS-MRV' or any(x in str(root).lower() for x in ['sp500-tracker-v13','sp500-tracker-5y']):raise ValueError('EXPECTED_ISOLATED_UEIS_MRV_ROOT')
 parent=a.within(root,'reports/step2B/MRV-INCREMENTAL-01');parent.mkdir(parents=True,exist_ok=True)
 out=parent/(dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:8]);out.mkdir()
 original_stdout,original_stderr=sys.stdout,sys.stderr;failed=False
 with (out/'run.log').open('w',encoding='utf-8') as log:
  sys.stdout=a.Tee(original_stdout,log);sys.stderr=a.Tee(original_stderr,log)
  try:
   print('OUTPUT='+str(out));print('PACKAGE_SELFTEST=PASS')
   a.js(out/'tests.json',tests);(out/'protocol.md').write_text(PROTOCOL,encoding='utf-8')
   a.js(out/'registration.json',{'version':VERSION,'specs':SPECS,'candidates':CANDIDATES,'frozen_controls':['F7','F6'],'calibration_controls':['C7','C6'],'test_years':list(range(2021,2026)),'lambda':LAMBDA,'parent_2A_manifest':PARENT,'risk':'HOLD','independent_validation':False})
   a.js(out/'runtime.json',{'python':sys.version,'platform':platform.platform(),'command':sys.argv,'script_sha256':sha(Path(source).read_bytes())})
   (out/'inputs').mkdir();(out/'inputs'/'parent-2A.zip').write_bytes(package['parent-2A.zip'])
   (out/'implementation').mkdir()
   for n in ['research.py','parent_runner.py','test_pipeline.py','synthetic-tests.json']:
    if n in package:(out/'implementation'/n).write_bytes(package[n])
   anchor=local_parent(root,a);a.js(out/'local-parent.json',anchor)
   fs,labs,models,preds,factors,params,repro=load(package,a)
   a.js(out/'baseline-reproduction.json',repro);a.js(out/'inherited-factor-parameters.json',params)
   plan=preflight_folds(labs,preds,factors);a.writecsv(out/'preflight-folds.csv',plan)
   if args.preflight:
    a.js(out/'result.json',{'engineering':'PASS','state':'PREFLIGHT_ONLY','new_real_model_fit':False,'risk':'HOLD'})
   else:
    metrics,review=run_study(labs,preds,factors,out,a)
    lines=['# MRV-step-2B 增量组合历史验证','', '工程PASS，候选结果待审核；risk=HOLD。已查看历史，不是新的独立step-3。','6增量候选、2校准对照、2冻结基线；系数训练、上一年校准、下一年测试严格分离。','C7/C6用于区分阈值/校准收益与新增信息收益；F7/F6保持原冻结模型。','', '|方案|2021—2025严重漏报|中等误报|轻度误报|严重预警天数|','|---|---:|---:|---:|---:|']
    for r in metrics:
     if r['period']=='2021-2025':lines.append('|%s|%d/%d|%d/%d|%d/%d|%d/%d|'%(r['id'],r['missed'],r['severe_n'],r['moderate_false'],r['moderate_n'],r['light_false'],r['light_n'],r['alarm_days'],r['n']))
    lines+=['','逐年结果见metrics.csv；补回与新增漏报见paired-comparisons.csv；精确模型与阈值见models。','某些校准年无非发布严重样本，不能声称该年召回已校准；见fold-audit.csv。','没有重新优化中等/轻度端点：未报严重时继承基线轻/中，原严重降级为中。','重大政策公告、信用、汇率等未合格历史输入没有纳入。','不要仅以整体均值选冠军；须看年度失效、新增漏报与轻度误报。所有候选须人工复核，不自动发布或替换M7/M6。','请回传evidence.zip。']
    (out/'REPORT.md').write_text('\n'.join(lines),encoding='utf-8')
    a.js(out/'result.json',{'engineering':'PASS','state':'COMPLETE_REVIEW_REQUIRED','candidate_count':6,'control_count':4,'test_years':list(range(2021,2026)),'fitted_artifacts':40,'risk':'HOLD','leading_model':None,'independent_validation':False,'original_M7_M6_unchanged':True})
   if local_parent(root,a)!=anchor:raise ValueError('LOCAL_PARENT_CHANGED_DURING_RUN')
   print('MRV_STEP_2B_INCREMENTAL=PASS');print('RISK_STATUS=HOLD')
  except Exception as ex:
   failed=True;traceback.print_exc();a.js(out/'result.json',{'engineering':'FAIL','state':'FAILED','risk':'HOLD','error':str(ex)})
  finally:sys.stdout,sys.stderr=original_stdout,original_stderr
 manifest={str(p.relative_to(out)):sha(p.read_bytes()) for p in sorted(out.rglob('*')) if p.is_file()}
 a.js(out/'manifest.json',manifest)
 with zipfile.ZipFile(out/'evidence.zip','w',zipfile.ZIP_DEFLATED) as z:
  for n in list(manifest)+['manifest.json']:z.write(out/n,n)
 print('EVIDENCE='+str(out/'evidence.zip'))
 if failed:raise SystemExit(1)
