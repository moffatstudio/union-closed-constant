import numpy as np, itertools
np.seterr(all='ignore')
rng=np.random.default_rng(5)
def h(p):
    p=np.asarray(p,float); o=np.zeros_like(p); m=(p>0)&(p<1)
    o[m]=-(p[m]*np.log2(p[m])+(1-p[m])*np.log2(1-p[m])); return o
def fid(x):
    x=np.asarray(x,float)
    return np.where(x<=0.5,x,np.where(x<=1/np.sqrt(2),np.sqrt(np.maximum(0.5-x*x,0)),0.0))
w=0.810222; c=0.38284; t0=0.006; rho=(1-t0)/h(np.array([t0]))[0]
PARTS={}
def parts(n):
    if n in PARTS: return PARTS[n]
    out=[]
    for a in itertools.product(range(3),repeat=n):
        out.append(np.array(a))
    PARTS[n]=out; return out
def Kupper(xs,ws):
    n=len(xs); best=np.inf; f=fid(xs); M=h(np.outer(xs,xs)+np.outer(f,f))
    for a in parts(n):
        tot=0.0
        for g in range(3):
            sel=np.where(a==g)[0]
            if len(sel)==0: continue
            pj=ws[sel]; m=pj.sum()
            if m<=0: continue
            P=pj/m; tot+=m*(P@M[np.ix_(sel,sel)]@P)
        best=min(best,tot)
    return best
worst=[np.inf,None]
def consider(xs,ws):
    xs=np.array(xs,float); ws=np.array(ws,float)
    if (ws<-1e-15).any(): return
    ws=np.clip(ws,0,None); s=ws.sum()
    if s<=0: return
    ws=ws/s
    if ws@xs<1-c-1e-14: return
    E=ws@h(xs)
    if E<=0: return
    R=(w*(ws@h(np.outer(xs,xs))@ws)+(1-w)*Kupper(xs,ws))/E
    sl=R-2*w*((1-c)-rho*E)
    if sl<worst[0]: worst[0]=sl; worst[1]=(xs.copy(),ws.copy(),R,E)
n=0
for y in list(np.logspace(-12,-0.001,60))+[0.9,0.98,0.99,0.9939,0.994,0.9941,0.999]:
    for z in np.logspace(-12,-0.5,30):
        consider([1.0,y,0.0],[1-c,z,max(0.0,1-(1-c)-z)]); n+=1
for t in [1e-9,1e-6,1e-4,0.003,0.006,0.0061,0.01,0.05]:
    for y in [1e-8,1e-4,0.01,0.5,0.9,0.994]:
        for z in np.logspace(-10,-1.5,18):
            for sig in [0.3,0.5,0.61716]:
                s=(1-c)-sig; rem=1-sig-s-z
                if s<0 or rem<0: continue
                consider([1.0,1-t,y,0.0],[sig,s,z,rem]); n+=1
for _ in range(4000):
    k=rng.integers(1,4)
    if rng.random()<0.5: mid=1-10.0**rng.uniform(-12,-1.5,size=k)
    else: mid=10.0**rng.uniform(-12,0,size=k)
    xs=np.clip(np.concatenate([[1.0],mid,[0.0]]),0,1)
    ws=rng.dirichlet(np.ones(len(xs)))*10.0**rng.uniform(-9,0,size=len(xs)); ws/=ws.sum()
    if ws@xs<1-c:
        need=1-c-ws@xs; j=int(np.argmin(xs)); mv=min(need/(1-xs[j]+1e-300),ws[j])
        ws[j]-=mv; ws[0]+=mv
    consider(list(xs),list(ws)); n+=1
print("laws tested:",n)
print("min (R - claimed bound) = %.6e"%worst[0])
xs,ws,R,E=worst[1]
print("worst: R=%.10f  bound=%.10f  E=%.3e"%(R,2*w*((1-c)-rho*E),E))
print("  atoms",np.round(xs,6)); print("  wts  ",ws)
