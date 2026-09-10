import numpy as np
from scipy.optimize import minimize
rng=np.random.default_rng(7)
w=0.810222; c=0.38284; C=1.00005
def h(x):
    x=np.asarray(x,float); out=np.zeros_like(x); m=(x>0)&(x<1); xx=x[m]
    out[m]=-(xx*np.log2(xx)+(1-xx)*np.log2(1-xx)); return out
def f(x):
    x=np.asarray(x,float); o=np.zeros_like(x)
    m1=x<=0.5; o[m1]=np.minimum(x[m1],1-x[m1])
    m2=(x>0.5)&(x<=2**-0.5); o[m2]=np.sqrt(np.maximum(0.5-x[m2]**2,0))
    return o
def W(xs):   # h(xy+f(x)f(y))
    X=xs[:,None]; Y=xs[None,:]
    return h(X*Y+f(xs)[:,None]*f(xs)[None,:])
def Wh(xs):
    return h(xs[:,None]*xs[None,:])
def Kupper(xs,m,J=3,ntry=6):
    """min over fractional assignments a_{ij} of sum_j (1/pi_j) a_j^T Wm a_j ; upper bd on Kmin"""
    n=len(xs); Wm=W(xs); best=float(m@Wm@m)  # J=1 (P=mu)
    for _ in range(ntry):
        z0=rng.normal(size=(n,J))
        def obj(z):
            A=np.exp(z.reshape(n,J)); A=A/A.sum(1,keepdims=True)*m[:,None]
            pi=A.sum(0); tot=0.0
            for j in range(J):
                if pi[j]>1e-14: tot+=float(A[:,j]@Wm@A[:,j])/pi[j]
            return tot
        res=minimize(obj,z0.ravel(),method='Nelder-Mead',
                     options={'maxiter':4000,'fatol':1e-15,'xatol':1e-10})
        best=min(best,res.fun)
    return max(best,0.0)
def R(xs,m,J=3):
    E=float(m@h(xs))
    if E<=0: return np.inf,0
    I=float(m@Wh(xs)@m)
    K=Kupper(xs,m,J)
    return (w*I+(1-w)*K)/E, E
# structured search: atoms {0,1,1-t,y,...}
best=[]
for trial in range(4000):
    k=rng.integers(1,4)
    xs=[0.0,1.0]
    for _ in range(k):
        u=rng.random()
        if u<0.45: xs.append(1-10**rng.uniform(-14,-1.5))   # near 1
        elif u<0.8: xs.append(10**rng.uniform(-14,-1.5))     # near 0
        else: xs.append(rng.uniform(0.02,0.98))
    xs=np.array(sorted(set(xs)))
    n=len(xs)
    # masses: put big mass on 1 and 0, tiny elsewhere
    m=rng.dirichlet(np.r_[np.full(n,0.3)])
    # bias: make the non-{0,1} masses tiny
    for i,x in enumerate(xs):
        if 0<x<1: m[i]*=10**rng.uniform(-8,0)
    m=m/m.sum()
    # enforce mean >= 1-c by shifting mass between 0 and 1
    mean=float(m@xs)
    if mean<1-c:
        i0=int(np.argmin(xs)); i1=int(np.argmax(xs))
        need=(1-c-mean)/(xs[i1]-xs[i0])
        if need>m[i0]: continue
        m[i0]-=need; m[i1]+=need
    E=float(m@h(xs))
    if not (0<E<=1e-4): continue
    r_,E=R(xs,m,J=2)
    best.append((r_,E,xs.copy(),m.copy()))
best.sort(key=lambda t:t[0])
print("n samples:",len(best))
for r_,E,xs,m in best[:8]:
    print(f"R={r_:.9f}  E={E:.3e}  C={C}  atoms={np.round(xs,12)} m={np.round(m,10)}")
print("\nmin R found:",best[0][0]," vs C=",C, " 2w(1-c)=",2*w*(1-c))
