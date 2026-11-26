"""Frozen J4, standard library inference only. Input: 26 consecutive completed SPX sessions."""
import hashlib,json,math,statistics
from decimal import Decimal
from pathlib import Path
HASH='af3c8b0bf1e761f239f9918b74be4cf78b9682f496c0470eb9747eb19b28ac87'
def bundle(root):
    raw=(root/'config/mrv/J4.json').read_bytes()
    if hashlib.sha256(raw).hexdigest()!=HASH:raise ValueError('J4_WEIGHTS_CHANGED')
    return json.loads(raw)
def features(rows,b):
    if len(rows)!=26:raise ValueError('J4_NEEDS_26_SESSIONS')
    for high,low,close,vix in rows:
        if not all(math.isfinite(x) and x>0 for x in [high,low,close,vix]) or not low<=close<=high:raise ValueError('J4_INPUT_INVALID')
    p=[r[2] for r in rows];v=[r[3] for r in rows];f={}
    ends=[]
    for prefix,series in [('p',p),('v',v)]:
        x=list(map(math.log,series));ret=[y-z for y,z in zip(x[1:],x)]
        for h in [1,5,10]:f[prefix+str(h)]=x[-1]-x[-1-h]
        f[prefix+'acc']=(x[-1]-x[-4])-(x[-4]-x[-7])
        f[prefix+'rv']=math.sqrt(statistics.mean(u*u for u in ret[-10:]));ends.append(ret[-10:])
        def ma(w,ago):
            end=len(series)-ago
            return math.log(statistics.mean(series[end-w:end]))
        for w in [5,10,20]:
            sl=(ma(w,0)-ma(w,3))/3
            f[f'{prefix.upper()}_s{w}']=sl;f[f'{prefix.upper()}_a{w}']=sl-(ma(w,3)-ma(w,6))/3
        for i,j in [(5,10),(10,20),(5,20)]:
            gap=ma(i,0)-ma(j,0)
            f[f'{prefix.upper()}_g{i}_{j}']=gap;f[f'{prefix.upper()}_w{i}_{j}']=gap-(ma(i,3)-ma(j,3))
    x,y=ends;mx,my=map(statistics.mean,ends)
    f['corr']=sum((i-mx)*(j-my) for i,j in zip(x,y))/math.sqrt(sum((i-mx)**2 for i in x)*sum((j-my)**2 for j in y))
    high,low,c,vl=rows[-1]
    f['prange']=math.log(high/low);f['ploc']=(c-low)/(high-low);f['logV']=math.log(vl)
    for w in [5,10,20]:f['spx_distance_ma'+str(w)]=c/statistics.mean(p[-w:])-1
    for pi in [1,-1]:
        for vi in [1,-1]:f[f'joint_{pi}_{vi}']=max(pi*f['p5']/(vl/100*math.sqrt(5/252)),0)*max(vi*f['v5'],0)
    for suf in ['s5','s10','s20','w5_10','w10_20']:
        pp,vv=[f[q+'_'+suf]/b['std'][q+'_'+suf] for q in 'PV']
        f['Xdiff_'+suf]=vv-pp;f['Xprod_'+suf]=vv*pp
    if set(f)!=set(b['cols']) or not all(math.isfinite(t) for t in f.values()):raise ValueError('J4_FEATURES_INVALID')
    return f
def infer(b,f):
    xx=[f[k] for k in b['cols']];scores=[]
    for s,trees in b['heads']:
        for tree in trees:
            node=tree[0]
            while len(node)>1:node=tree[node[2] if xx[node[0]]<=node[1] else node[3]]
            s+=node[0]
        scores.append(1/(1+math.exp(-s)))
    n,s=scores;g,t=b['cut']
    return n,s,'severe' if s>t else 'light' if n<=g else 'moderate'
def label(close,low):
    c,l=map(lambda t:Decimal(str(t)),(close,low))
    if min(c,l)<=0:raise ValueError('BAD_PRICE')
    d=max(Decimal(0),1-l/c)
    return float(d),'severe' if d>Decimal('.025') else 'moderate' if d>Decimal('.012') else 'light'
