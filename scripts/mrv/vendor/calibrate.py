"""Small constrained convex calibrators; Python3.9 stdlib, no class weighting."""
import math,statistics as st
EPS=1e-8
SPECS={'P1_LOGIT':('logit',.01),'P2_BETA':('beta',.01),'P3_EVENT':('event',.01),'P1_L001':('logit',.001),'P1_L100':('logit',.1)}
PRIMARY=['P1_LOGIT','P2_BETA','P3_EVENT']
CLASSES=['light','moderate','severe']
def sig(v):
 if v>=0:return 1/(1+math.exp(-v))
 a=math.exp(v);return a/(1+a)
def soft(v):return max(0,v)+math.log1p(math.exp(-abs(v)))
def raw(s,event,kind):
 s=min(1-EPS,max(EPS,s));l=math.log(s);u=-math.log1p(-s)
 return [l,u] if kind=='beta' else [l+u,float(event)] if kind=='event' else [l+u]
def solve(a,b):
 n=len(b);m=[list(r)+[v] for r,v in zip(a,b)]
 for j in range(n):
  k=max(range(j,n),key=lambda k:abs(m[k][j]))
  if abs(m[k][j])<1e-15:raise ValueError('SINGULAR_HESSIAN')
  m[k],m[j]=m[j],m[k];v=m[j][j];m[j]=[x/v for x in m[j]]
  for i in range(n):
   if i==j:continue
   t=m[i][j]
   for k in range(j,n+1):m[i][k]-=t*m[j][k]
 return [r[-1] for r in m]
def objective(X,y,b,lam):return sum(soft(sum(u*v for u,v in zip(x,b)))-t*sum(u*v for u,v in zip(x,b)) for x,t in zip(X,y))/len(y)+lam/2*sum(v*v for v in b[1:])
def derivatives(X,y,b,lam):
 n=len(y);q=len(b);g=[0.]*q;h=[[0.]*q for _ in range(q)]
 for x,t in zip(X,y):
  p=sig(sum(u*v for u,v in zip(x,b)));r=p-t;w=p*(1-p)
  for j in range(q):
   g[j]+=r*x[j]/n
   for k in range(j+1):h[j][k]+=w*x[j]*x[k]/n
 for j in range(q):
  if j:g[j]+=lam*b[j];h[j][j]+=lam
  for k in range(j):h[k][j]=h[j][k]
 return g,h
def fit_numeric(X,y,lam,nonnegative):
 if len(set(y))<2:raise ValueError('BINARY_CLASS_ABSENT')
 p=st.mean(y);b=[math.log(p/(1-p))]+[0.]*(len(X[0])-1)
 for it in range(150):
  g,h=derivatives(X,y,b,lam)
  kkt=max(abs(min(0,g[j])) if j in nonnegative and b[j]<=1e-12 else abs(g[j]) for j in range(len(b)))
  if kkt<=1e-7:return {'coef':b,'iterations':it,'kkt':kkt,'objective':objective(X,y,b,lam),'converged':True}
  active=[j for j in range(len(b)) if not (j in nonnegative and b[j]<=1e-12 and g[j]>=0)]
  stepv=solve([[h[j][k] for k in active] for j in active],[g[j] for j in active]);delta=[0.]*len(b)
  for j,v in zip(active,stepv):delta[j]=v
  old=objective(X,y,b,lam);accepted=False
  for method in range(2):
   if method:delta=g[:]
   step=1.
   for _ in range(45):
    trial=[max(0,v-step*d) if j in nonnegative else v-step*d for j,(v,d) in enumerate(zip(b,delta))]
    displacement=sum(g[j]*(trial[j]-b[j]) for j in range(len(b)))
    if displacement<0 and objective(X,y,trial,lam)<=old+1e-4*displacement+1e-15:
     b=trial;accepted=True;break
    step*=.5
   if accepted:break
  if not accepted:raise ValueError('CALIBRATION_LINE_SEARCH')
 raise ValueError('CALIBRATION_NOT_CONVERGED')
def fit_stage(rr,kind,lam,conditional=False):
 data=[r for r in rr if not conditional or r['class']!='light'];y=[int(r['class']=='severe' if conditional else r['class']!='light') for r in data]
 info={'n':len(data),'positive_n':sum(y),'negative_n':len(y)-sum(y),'conditional':conditional}
 if len(set(y))<2:return dict(info,status='BLOCKED_CLASS_ABSENT')
 X=[raw(r['score'],bool(r['events']),kind) for r in data];q=len(X[0]);means=[st.mean(x[j] for x in X) for j in range(q)];sd=[st.pstdev(x[j] for x in X) for j in range(q)]
 # Event is a binary predictor; continuous slopes are constrained monotonically increasing.
 if kind=='event':means[-1]=0.;sd[-1]=1.
 sd=[v if v>1e-12 else 1. for v in sd]
 xx=[[1.]+[(v-m)/s for v,m,s in zip(x,means,sd)] for x in X];positive=list(range(1,q+1-(kind=='event')))
 fitted=fit_numeric(xx,y,lam,positive)
 return dict(info,status='FIT',kind=kind,lambda_=lam,means=means,sd=sd,nonnegative=positive,model=fitted)
def fit(rr,name):
 counts=[sum(r['class']==c for r in rr) for c in CLASSES];freq=[(n+.5)/(len(rr)+1.5) for n in counts]
 out={'id':name,'n':len(rr),'counts':counts,'first_date':min(r['date'] for r in rr),'last_date':max(r['date'] for r in rr),'train_dates':[r['date'] for r in rr],'score_min':min(r['score'] for r in rr),'score_max':max(r['score'] for r in rr),'prior_severe_only':counts[2]==0}
 if name in ['FREQ','GRADE_FREQ']:
  by={}
  for grade in CLASSES:
   sub=[r for r in rr if r['final_grade']==grade];by[grade]=[(sum(r['class']==c for r in sub)+20*f)/(len(sub)+20) for c,f in zip(CLASSES,freq)]
  return dict(out,status='FIT',frequency=freq,grade_frequency=by)
 kind,lam=SPECS[name];a=fit_stage(rr,kind,lam);b=fit_stage(rr,kind,lam,True)
 return dict(out,status='FIT' if a['status']==b['status']=='FIT' else 'PARTIAL_OR_BLOCKED',stage_a=a,stage_b=b)
def stage_predict(art,r):
 if art['status']!='FIT':return None
 x=raw(r['score'],bool(r['events']),art['kind']);x=[1.]+[(v-m)/s for v,m,s in zip(x,art['means'],art['sd'])]
 return sig(sum(v*b for v,b in zip(x,art['model']['coef'])))
def predict(art,r):
 if art['id'] in ['FREQ','GRADE_FREQ']:
  p=art['frequency'] if art['id']=='FREQ' else art['grade_frequency'][r['final_grade']];return p+[p[1]+p[2]]
 q=stage_predict(art['stage_a'],r);u=stage_predict(art['stage_b'],r)
 if q is None:return [None]*4
 if u is None:return [1-q,None,None,q]
 return [1-q,q*(1-u),q*u,q]
def check(p):
 if any(v is not None and (not math.isfinite(v) or v<0 or v>1) for v in p):raise ValueError('PROBABILITY_BOUNDS')
 if all(v is not None for v in p):
  if abs(sum(p[:3])-1)>1e-12 or abs(p[1]+p[2]-p[3])>1e-12 or p[2]>p[3]+1e-12:raise ValueError('PROBABILITY_COHERENCE')
def quant(v,q):
 if not v:return None
 v=sorted(v);return v[max(0,math.ceil(q*len(v))-1)]
def block_indices(rr,length,rng):
 groups={}
 for i,r in enumerate(rr):groups.setdefault(r['date'][:4],[]).append(i)
 out=[]
 for year,indices in sorted(groups.items()):
  n=len(indices);L=min(n,length);part=[]
  while len(part)<n:
   start=rng.randrange(n-L+1);part.extend(indices[start:start+L])
  out.extend(part[:n])
 return out
