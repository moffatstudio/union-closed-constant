import numpy as np, itertools, time
rng=np.random.default_rng(11)
w=0.810222; c=0.38284; C=1.00005
def h(x):
    x=np.asarray(x,float); out=np.zeros_like(x); m=(x>0)&(x<1); xx=x[m]
    out[m]=-(xx*np.log2(xx)+(1-xx)*np.log2(1-xx)); return out
def fv(x):
    x=np.asarray(x,float); o=np.zeros_like(x)
    m1=x<=0.5; o[m1]=np.minimum(x[m1],1-x[m1])
    m2=(x>0.5)&(x<=2**-0.5); o[m2]=np.sqrt(np.maximum(0.5-x[m2]**2,0))
    return o
def mats(xs):
    Wh=h(xs[:,None]*xs[None,:])
    Wk=h(np.clip(xs[:,None]*xs[None,:]+fv(xs)[:,None]*fv(xs)[None,:],0,1))
    return Wh,Wk
def Kup(xs,m,Wk,maxg=3):
    n=len(xs); best=float(m@Wk@m)
    for g in range(2,min(maxg,n)+1):
        for lab in itertools.product(range(g),repeat=n):
            if len(set(lab))<g: continue
            tot=0.0
            for j in range(g):
                idx=[i for i in range(n) if lab[i]==j]
                a=m[idx]; p=a.sum()
                if p>0: tot+=float(a@Wk[np.ix_(idx,idx)]@a)/p
            best=min(best,tot)
    return best
def Rval(xs,m):
    E=float(m@h(xs))
    if E<=0: return np.inf,0.0
    Wh,Wk=mats(xs)
    I=float(m@Wh@m); K=Kup(xs,m,Wk)
    return (w*I+(1-w)*K)/E, E
best=[]; t0=time.time()
while time.time()-t0<100:
    k=rng.integers(1,4); xs=[0.0,1.0]
    for _ in range(k):
        u=rng.random()
        if u<0.4: xs.append(1-10**rng.uniform(-13,-1.2))
        elif u<0.75: xs.append(10**rng.uniform(-13,-1.2))
        else: xs.append(rng.uniform(0.02,0.98))
    xs=np.array(sorted(set(xs))); n=len(xs)
    m=rng.dirichlet(np.full(n,0.4))
    for i,x in enumerate(xs):
        if 0<x<1: m[i]*=10**rng.uniform(-9,0)
    m=m/m.sum()
    mean=float(m@xs)
    if mean<1-c:
        need=(1-c-mean)/(xs[-1]-xs[0])
        if need>m[0]: continue
        m[0]-=need; m[-1]+=need
    E=float(m@h(xs))
    if not (0<E<=1e-4): continue
    r_,E=Rval(xs,m); best.append((r_,E,xs,m))
best.sort(key=lambda t:t[0])
print("samples:",len(best)," 2w(1-c)=",2*w*(1-c)," C=",C)
for r_,E,xs,m in best[:10]:
    print(f"R={r_:.10f} E={E:.3e} atoms={np.array2string(xs,precision=10)} m={np.array2string(m,precision=8)}")
