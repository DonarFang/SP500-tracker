import argparse,csv,datetime as dt,hashlib,io,json,math,platform,sys,traceback,uuid,zipfile
from pathlib import Path
VERSION='MRV-step-3-FourScore-v1.0'
PARENT='ee23bf546c612e86527f45bcbf26022b8cf61e1ccf94dcc942236d35f5503254'
SELECTED={'LINEAR4_T2021_2022':('original','LINEAR4'),'QUAD4_T2020_2022':('extended','QUAD4')}
PROTOCOL='''# MRV-step-3 四分数候选冻结与验证审计
候选LINEAR4_T2021_2022、QUAD4_T2020_2022，分别继承2B原训练版与2020扩展训练版PRIMARY的完整变换、系数、2023阈值。禁止本轮重拟合、重新校准、采用2025事后阈值或择优情景。M7/M6/原阈值OR为固定对照。
本脚本完成step-3入口工作：冻结快照、2024—2025历史逐日预测复现、标签/日历/指标核验、本地已索引文件的新日期覆盖审计。不能把已看过的2024—2025复用为独立验证。无合格独立队列时research=HOLD_INSUFFICIENT_INDEPENDENT_DATA，不生成验证通过或leading。
2020—2022为组合训练/研究；2023校准；2024—2025已参与研究选择。2019—2020还参与底层训练/校准。当前来源是历史EOD代理，未认证历史实时vintage。
预测信息截至T交易日收盘；目标下一交易日。标签max(0,1-目标最低/前收)：严重>=3%，中等>1.2%且<3%，轻度<=1.2%。CPI/NFP/预定FOMC仅发布日覆盖严重；发布日完整排除中等/轻度误报，所有严重日保留。输出模型、日历、组合贡献。
整体非发布中等误报<=20%；年度超标单列，非新增硬门槛。零漏报为目标但非硬否决。轻度误报、连续报警、样本量同时报告；0/0为空。工程PASS不等于模型验证PASS。
底层M7/M6参数冻结；I7R/I6V沿用年度扩展训练规则：目标Y年用2019至Y-2训练、Y-1校准。四分数输入只有连续分数，底层等级阈值不参与组合评分。组合层2023校准的阈值不更新。未来任何年度底层拟合必须单独保存时间边界及来源审计；不能直接把2025底层参数当成完整未来规则。
本轮不读取新年份价格标签来调参或选择候选；本地审计仅检查索引、哈希、字段、日期覆盖。即使发现2026原始数据，也不自动视为未查看、已认证或可直接验证的四分数队列。
下一步必须明确2026或更晚共同覆盖、事件日历、底层年度模型、历史可得性、是否曾参与选择及预测截止时点。旧历史不能通过改名变成独立样本。真正冻结后的前瞻证据还需提前留存预测。
离线Python3.9标准库。仅写UEIS-MRV/reports/step3/MRV-FOURSCORE-01新目录。不修改原step3、旧报告、v13、Forward、Live或系统依赖。
'''
def sha(b):return hashlib.sha256(b).hexdigest()
def js(path,x):path.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8')
def rows(b):return list(csv.DictReader(io.StringIO(b.decode('utf-8-sig'))))
def csvout(path,rr):
 if not rr:path.write_text('',encoding='utf-8');return
 keys=list(dict.fromkeys(k for r in rr for k in r))
 with path.open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=keys);w.writeheader()
  for r in rr:w.writerow({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(list,dict)) else v for k,v in r.items()})
def archive(blob,expected=None):
 z=zipfile.ZipFile(io.BytesIO(blob));names=z.namelist()
 if len(names)!=len(set(names)) or z.testzip():raise ValueError('ZIP_INTEGRITY')
 if expected and sha(z.read('manifest.json'))!=expected:raise ValueError('MANIFEST_IDENTITY')
 for n,h in json.loads(z.read('manifest.json')).items():
  if Path(n).is_absolute() or '..' in Path(n).parts or sha(z.read(n))!=h:raise ValueError('MANIFEST_FILE:'+n)
 return z
def safe(root,rel):
 if Path(rel).is_absolute() or '..' in Path(rel).parts:raise ValueError('UNSAFE_PATH')
 p=root/rel
 if any(x.is_symlink() for x in [p]+list(p.parents) if x!=root and root in x.parents):raise ValueError('SYMLINK_REFUSED')
 if root!=p.resolve() and root not in p.resolve().parents:raise ValueError('PATH_ESCAPE')
 return p
def score(art,r):
 vals=[float(r[k]) for k in ['F7','F6','I7R','I6V']]
 if any(not math.isfinite(v) or v<0 or (i!=1 and v>1) for i,v in enumerate(vals)):raise ValueError('BAD_SCORE')
 x=[v if i==1 else math.log(max(1e-8,v)/max(1e-8,1-v)) for i,v in enumerate(vals)]
 x=[0. if p['kind']=='constant' else math.asinh((v-p['median'])/p['scale']) for v,p in zip(x,art['scaler'])]
 if art['kind']=='QUAD4':x=x+[x[i]*x[j] for i in range(4) for j in range(i,4)]
 elif art['kind']!='LINEAR4':raise ValueError('MODEL_KIND')
 v=art['model']['coef'][0]+sum((v-m)/s*b for v,m,s,b in zip(x,art['mean'],art['sd'],art['model']['coef'][1:]))
 return 1/(1+math.exp(-v)) if v>=0 else math.exp(v)/(1+math.exp(v))
def measure(rr):
 sev=[r for r in rr if r['class']=='severe'];mid=[r for r in rr if r['class']=='moderate' and not r['events']];light=[r for r in rr if r['class']=='light' and not r['events']]
 best=run=0
 for r in rr:
  run=run+1 if r['combined_alarm'] else 0;best=max(best,run)
 def rate(n,d):return n/d if d else None
 mm=sum(r['model_alarm'] for r in mid);ll=sum(r['model_alarm'] for r in light)
 return {'n':len(rr),'severe_n':len(sev),'combined_missed':sum(not r['combined_alarm'] for r in sev),'model_only_missed':sum(not r['model_alarm'] for r in sev),'event_only_missed':sum(not r['events'] for r in sev),'non_event_severe_n':sum(not r['events'] for r in sev),'non_event_missed':sum(not r['model_alarm'] and not r['events'] for r in sev),'moderate_n':len(mid),'moderate_false':mm,'moderate_false_rate':rate(mm,len(mid)),'light_n':len(light),'light_false':ll,'light_false_rate':rate(ll,len(light)),'alarm_days':sum(r['combined_alarm'] for r in rr),'longest_alarm_run':best}
def inventory(root):
 p=safe(root,'config/data-index.json');out=[]
 if not p.exists():return [{'status':'INDEX_NOT_FOUND','qualification':'UNVERIFIED_NOT_ABSENT'}]
 data=json.loads(p.read_text());files=data.get('files',{})
 if not isinstance(files,dict):raise ValueError('INDEX_SCHEMA')
 for key,rec in files.items():
  if not isinstance(rec,dict) or not str(rec.get('path','')).endswith('.csv'):continue
  rel=rec['path'];f=safe(root,rel);r={'index_key':key,'path':rel,'qualification':'DATE_COVERAGE_ONLY_NOT_INDEPENDENT_VALIDATION'}
  if not f.is_file():r['status']='MISSING';out.append(r);continue
  b=f.read_bytes();r['sha256']=sha(b);r['indexed_hash_match']=sha(b)==rec.get('sha256');r['status']='READ'
  try:
   rr=rows(b);dates=[]
   for row in rr:
    for col in ['date','Date','target_date','feature_date','observation_date']:
     v=row.get(col,'')
     if len(v)==10:
      try:dt.date.fromisoformat(v);dates.append(v);break
      except ValueError:pass
   r.update(rows=len(rr),first_date=min(dates) if dates else None,last_date=max(dates) if dates else None,rows_after_2025=sum(d>'2025-12-31' for d in dates),columns=list(rr[0]) if rr else [])
  except (UnicodeError,csv.Error):r['status']='UNREADABLE_CSV'
  out.append(r)
 return out

def validate(z,out):
 parent=archive(z.read('inputs/parent.zip'),'c1ce1a53e371a576ee0d59a0f364b131d7a229e82634fc45df78e2431050e3f6')
 a=archive(parent.read('inputs/parent-2A.zip'));v=archive(a.read('inputs/parent-3.zip'))
 # Independently recompute labels from archived SPX price bases.
 labels={}
 for r in rows(v.read('labels.csv')):
  d=r['date'];loss=max(0,1-float(r['target_low'])/float(r['previous_close']));cl='severe' if loss>=.03 else 'moderate' if loss>.012 else 'light'
  if cl!=r['class'] or abs(loss-float(r['loss']))>1e-12:raise ValueError('SPX_LABEL_MISMATCH')
  labels[d]=(loss,cl,json.loads(r['events']),r['feature_date'])
 inputs=rows(z.read('four-score-inputs.csv'));dd={r['date']:r for r in inputs}
 if len(dd)!=len(inputs):raise ValueError('DUPLICATE_INPUT_DATE')
 dates=sorted(d for d in dd if '2024'<=d[:4]<='2025')
 if len(dates)!=502 or set(dates)!=set(d for d in labels if '2024'<=d[:4]<='2025'):raise ValueError('TEST_COHORT')
 for d in dates:
  r=dd[d];loss,cl,ev,fd=labels[d]
  if r['class']!=cl or abs(float(r['loss'])-loss)>1e-12 or json.loads(r['events'])!=ev or r['feature_date']!=fd or not fd<d:raise ValueError('LABEL_OR_TIME_ALIGNMENT')
 (out/'frozen').mkdir();allpred=[];locks=[]
 original=[r for r in rows(z.read('original/predictions.csv')) if r['scenario']=='PRIMARY'];controls={k:{r['date']:r for r in original if r['model']==k} for k in ['M7','M6','OR']}
 for ident,(part,kind) in SELECTED.items():
  n=part+'/models/'+kind+'__PRIMARY.json';blob=z.read(n);art=json.loads(blob)
  if art['kind']!=kind or art['input_order']!=['F7','F6','I7R','I6V'] or art['scenario']!='PRIMARY' or art['lambda']!=.01 or art['comparison']!='>':raise ValueError('FROZEN_CONTRACT')
  years={d[:4] for d in art['train_dates']}
  if years!=({'2021','2022'} if kind=='LINEAR4' else {'2020','2021','2022'}) or {d[:4] for d in art['calibration_dates']}!={'2023'}:raise ValueError('FROZEN_TRAIN_DATES')
  dest=out/'frozen'/(ident+'.json');dest.write_bytes(blob);h=sha(blob)
  ref={r['date']:r for r in rows(z.read(part+'/predictions.csv')) if r['model']==kind and r['scenario']=='PRIMARY'}
  if set(ref)!=set(dates):raise ValueError('REF_COHORT')
  maxerr=0
  for d in dates:
   s=score(art,dd[d]);err=abs(s-float(ref[d]['score']));maxerr=max(err,maxerr);alarm=s>art['threshold'];ev=labels[d][2]
   if err>1e-12 or alarm!=(ref[d]['model_grade']=='severe') or (alarm or bool(ev))!=(ref[d]['final_grade']=='severe'):raise ValueError('PREDICTION_MISMATCH')
   allpred.append({'model':ident,'date':d,'feature_date':labels[d][3],'class':labels[d][1],'loss':labels[d][0],'events':ev,'score':s,'threshold':art['threshold'],'model_alarm':alarm,'combined_alarm':alarm or bool(ev),'parameter_sha256':h})
  if sha(dest.read_bytes())!=h:raise ValueError('FROZEN_CHANGED')
  locks.append({'id':ident,'source':n,'sha256':h,'threshold':art['threshold'],'rows_reproduced':len(dates),'max_score_error':maxerr,'fit_called':False})
 for ident in ['M7','M6','OR','EVENT_ONLY']:
  for d in dates:
   ev=labels[d][2];alarm=False if ident=='EVENT_ONLY' else controls[ident][d]['model_grade']=='severe'
   allpred.append({'model':ident,'date':d,'feature_date':labels[d][3],'class':labels[d][1],'loss':labels[d][0],'events':ev,'score':None,'threshold':None,'model_alarm':alarm,'combined_alarm':alarm or bool(ev),'parameter_sha256':'parent_frozen_control'})
 metrics=[]
 for ident in list(SELECTED)+['M7','M6','OR','EVENT_ONLY']:
  for period in ['2024','2025','2024-2025']:
   rr=[r for r in allpred if r['model']==ident and (period=='2024-2025' or r['date'].startswith(period))];metrics.append({'model':ident,'period':period,'evidence_type':'REUSED_HISTORY_NOT_INDEPENDENT',**measure(rr)})
 csvout(out/'predictions.csv',allpred);csvout(out/'metrics.csv',metrics);js(out/'freeze-lock.json',locks)
 # Snapshot complete source artifacts, including annual bottom-model and frozen-base chain.
 js(out/'bottom-model-policy.json',{'M7_M6':'frozen inherited models','I7R_I6V':'target year Y: train2019..Y-2; calibrationY-1; use continuous score only','future_bottom_models_not_created':True,'source':'inputs/parent.zip nested complete evidence chain','top_layer_update_allowed':False})
 return metrics,locks

def selftest():
 art={'kind':'LINEAR4','scaler':[{'kind':'constant'}]*4,'mean':[0]*4,'sd':[1]*4,'model':{'coef':[0]*5}}
 assert score(art,dict(F7=.5,F6=.5,I7R=.5,I6V=.5))==.5
 try:score(art,dict(F7=float('nan'),F6=.1,I7R=.1,I6V=.1));raise AssertionError('nan accepted')
 except ValueError:pass
 rr=[{'class':'moderate','events':['CPI'],'model_alarm':True,'combined_alarm':True},{'class':'severe','events':['CPI'],'model_alarm':False,'combined_alarm':True},{'class':'light','events':[],'model_alarm':True,'combined_alarm':True}]
 m=measure(rr);assert m['moderate_n']==0 and m['moderate_false_rate'] is None and m['severe_n']==1 and m['model_only_missed']==1 and m['combined_missed']==0 and m['light_false']==1 and m['longest_alarm_run']==3
 assert measure([])['moderate_false_rate'] is None
 return {'status':'PASS','checks':['constant_score','nonfinite_refused','release_excluded_false_denominator','release_severe_retained','model_calendar_separate','zero_denominator_null','light_alarm_count','consecutive_alarm_count']}
def finalize(out):
 manifest={str(p.relative_to(out)):sha(p.read_bytes()) for p in sorted(out.rglob('*')) if p.is_file() and p.name not in ['manifest.json','evidence.zip']};js(out/'manifest.json',manifest)
 with zipfile.ZipFile(out/'evidence.zip','w',zipfile.ZIP_DEFLATED) as z:
  for n in list(manifest)+['manifest.json']:z.write(out/n,n)
 print('EVIDENCE='+str(out/'evidence.zip'))
def main(package,source):
 ap=argparse.ArgumentParser();ap.add_argument('--root',default=str(Path.home()/'UEIS-MRV'));ap.add_argument('--self-test',action='store_true');args=ap.parse_args();tests=selftest()
 if args.self_test:print(json.dumps(tests));return
 raw=Path(args.root).expanduser()
 if raw.is_symlink():raise ValueError('ROOT_SYMLINK')
 root=raw.resolve()
 if root.name!='UEIS-MRV' or not root.is_dir() or any(k in str(root).lower() for k in ['sp500-tracker-v13','sp500-tracker-5y']):raise ValueError('ISOLATED_MRV_ROOT_REQUIRED')
 base=safe(root,'reports/step3/MRV-FOURSCORE-01');base.mkdir(parents=True,exist_ok=True);out=base/(dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:8]);out.mkdir();failed=False
 print('OUTPUT='+str(out))
 try:
  (out/'protocol.md').write_text(PROTOCOL,encoding='utf-8');js(out/'tests.json',tests);js(out/'runtime.json',{'version':VERSION,'python':sys.version,'platform':platform.platform(),'script_sha256':sha(Path(source).read_bytes()),'args':sys.argv})
  (out/'implementation').mkdir();(out/'implementation'/'runner.py').write_bytes(package['runner.py']);(out/'inputs').mkdir();(out/'inputs'/'parent.zip').write_bytes(package['parent.zip'])
  z=archive(package['parent.zip'],PARENT)
  if json.loads(z.read('result.json'))['engineering']!='PASS':raise ValueError('PARENT_FAILED')
  js(out/'registration.json',{'selected':SELECTED,'parent_manifest':PARENT,'refit_allowed':False,'recalibration_allowed':False,'replay_years':[2024,2025],'independent_years':[],'risk':'HOLD'})
  metrics,locks=validate(z,out);inv=inventory(root);csvout(out/'local-data-coverage.csv',inv)
  js(out/'independence-audit.json',{'qualified_independent_rows':0,'bundled_four_scores_last':'2025-12-31','status':'NOT_ESTABLISHED','local_raw_presence_does_not_establish_independence':True,'local_indexed_files_with_post2025_dates':sum(r.get('rows_after_2025',0)>0 for r in inv),'missing_requirements':['approved untouched common cohort','verified source availability and event calendar','audited annual bottom models and four scores','frozen evaluation dates and no post-outcome tuning'],'future_raw_data_scored':False})
  lines=['# MRV-step-3 四分数入口审计','工程PASS；候选冻结与历史复现完成。','**独立验证尚未完成：HOLD_INSUFFICIENT_INDEPENDENT_DATA。**','2024—2025已参与选择，仅列历史复现；本地文件日期覆盖不等于独立样本认证。','', '|候选/对照|严重漏报（含日历）|模型单独漏报|中等误报|轻度误报|预警日|','|---|---:|---:|---:|---:|---:|']
  for r in metrics:
   if r['period']=='2024-2025':lines.append('|%s|%d/%d|%d/%d|%d/%d|%d/%d|%d|'%(r['model'],r['combined_missed'],r['severe_n'],r['model_only_missed'],r['severe_n'],r['moderate_false'],r['moderate_n'],r['light_false'],r['light_n'],r['alarm_days']))
  lines+=['','下一步：依据local-data-coverage.csv审计2026或更晚的共同输入、日历及历史使用记录，再冻结独立验证区间；尚未获得这些证据，不能宣称模型验证通过。','所有参数不变，未采用事后阈值，未产生生产交易许可。原M7/M6的既有step-3记录不被覆盖。','请回传evidence.zip。'];(out/'REPORT.md').write_text('\n'.join(lines),encoding='utf-8')
  js(out/'result.json',{'engineering':'PASS','stage':'MRV-step-3','state':'FREEZE_AND_REPLAY_COMPLETE','research':'HOLD_INSUFFICIENT_INDEPENDENT_DATA','independent_validation_completed':False,'independent_n':0,'risk':'HOLD','leading_model':None});print('ENGINEERING=PASS\nRESEARCH=HOLD_INSUFFICIENT_INDEPENDENT_DATA')
  (out/'run.log').write_text('SELFTEST=PASS\nPARENT_MANIFEST=PASS\nFROZEN_REPLAY=PASS\nENGINEERING=PASS\nRESEARCH=HOLD_INSUFFICIENT_INDEPENDENT_DATA\n')
 except Exception as e:
  failed=True;(out/'run.log').write_text(traceback.format_exc());js(out/'result.json',{'engineering':'FAIL','error':str(e),'risk':'HOLD'});traceback.print_exc()
 finalize(out)
 if failed:raise SystemExit(1)
