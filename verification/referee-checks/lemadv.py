import numpy as np, itertools
np.seterr(all='ignore')
rng=np.random.default_rng(11)
def h(p):
    p=np.asarray(p,float); o=np.zeros_like(p); m=(p>0)&(p<1)
    o[m]=-(p[m]*np.log2(p[m])+(1-p[m])*np.log2(1-p[m])); return o
def fid(x):
    x=np.asarray(x,float)
    return np.where(x<=0.5,x,np.where(x<=1/np.sqrt(2),np.sqrt(np.maximum(0.5-x*x,0)),0.0))
w=0.810222; c=0.38284; t0=0.006; rho=(1-t0)/h(np.array([t0]))[0]
def Kupper(xs,ws):
    n=len(xs); best=np.inf
    for ngr in (1,2,3):
        for assign in itertools.product(range(ngr),repeat=n):
            if len(set(assign))!=ngr: continue
            tot=0.0
            for gidx in range(ngr):
                sel=[i for i in range(n) if assign[i]==gidx]
                pj=ws[sel]; m=pj.sum()
                if m<=0: continue
                P=pj/m; b=xs[sel]; f=fid(b)
                tot+=m*(P@h(np.outer(b,b)+np.outer(f,f))@P)
            best=min(best,tot)
    return best
def test(xs,ws):
    ws=ws/ws.sum(); mean=ws@xs
    if mean<1-c-1e-15: return None
    E=ws@h(xs)
    if E<=0: return None
    I=ws@h(np.outer(xs,xs))@ws
    R=(w*I+(1-w)*Kupper(xs,ws))/E
    return R, 2*w*((1-c)-rho*E), E
worst=np.inf; worstcase=None; nt=0
def consider(xs,ws):
    global worst,worstcase,nt
    r=test(np.array(xs,float),np.array(ws,float))
    if r is None: return
    nt+=1
    slack=r[0]-r[1]
    if slack<worst: worst=slack; worstcase=(xs,ws,r)
# structured families
for y in list(np.logspace(-12,-0.001,120))+list(np.linspace(0.9,0.9999,60))+[0.994,0.9939,0.9941,0.99,0.98,0.95]:
    for z in np.logspace(-12,-0.5,60):
        m0=1-(1-c)-z
        if m0<0: continue
        consider([1.0,y,0.0],[1-c,z,m0])
for t in [1e-9,1e-6,1e-4,0.003,0.006,0.0061,0.007,0.01,0.05]:
    for y in [1e-8,1e-4,0.01,0.3,0.7,0.9,0.994]:
        for z in np.logspace(-10,-1,40):
            for sig in [0.3,0.5,0.61716,0.7]:
                x=[1.0,1-t,y,0.0]; ww=[sig,(1-c)-sig*1.0-0.0,z,0]
                s=(1-c)-sig
                if s<0 or s>1: continue
                rem=1-sig-s-z
                if rem<0: continue
                consider([1.0,1-t,y,0.0],[sig,s,z,rem])
# random small-entropy laws
for _ in range(9000):
    k=rng.integers(2,6)
    xs=np.concatenate([[1.0],1-10.0**rng.uniform(-12,-1.5,size=k-1)]) if rng.random()<0.5 \
       else np.concatenate([[1.0],10.0**rng.uniform(-12,0,size=k-1)])
    xs=np.clip(np.concatenate([xs,[0.0]]),0,1)
    ws=rng.dirichlet(np.ones(len(xs)))*10.0**rng.uniform(-9,0,size=len(xs))
    ws=ws/ws.sum()
    # push mean up to feasibility by shifting mass to the atom at 1
    if ws@xs<1-c:
        need=(1-c-ws@xs)/(1-min(xs))
        j=int(np.argmin(xs)); ws=ws.copy()
        mv=min(need,ws[j]); ws[j]-=mv; ws[0]+=mv
    consider(list(xs),list(ws))
print("laws tested:",nt)
print("min (R - claimed bound) =",worst)
xs,ws,r=worstcase
print("worst case: R=%.10f bound=%.10f E=%.3e"%(r[0],r[1],r[2]))
print("  atoms",np.round(np.array(xs,float),6)); print("  wts  ",np.array(ws,float))
