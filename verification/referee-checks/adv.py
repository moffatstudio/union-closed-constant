import numpy as np
from math import sqrt
from scipy.optimize import minimize
rng=np.random.default_rng(0)
def h(p):
    p=np.asarray(p,float); out=np.zeros_like(p)
    m=(p>1e-300)&(p<1-1e-16); out[m]=-p[m]*np.log2(p[m])-(1-p[m])*np.log2(1-p[m]); return out
def fid(x):
    x=np.asarray(x,float)
    return np.where(x<=0.5,x,np.where(x<=1/sqrt(2),np.sqrt(np.maximum(0.5-x*x,0.0)),0.0))
W=0.810222099; B=1-W
def ratio(v,c,natoms,floor):
    n=natoms
    # params: q, weights0(n), atoms0(n), weights1(n), atoms1(n)
    q=1/(1+np.exp(-v[0]))
    a0=np.exp(v[1:1+n]); a0/=a0.sum()
    b0=1/(1+np.exp(-v[1+n:1+2*n]))
    a1=np.exp(v[1+2*n:1+3*n]); a1/=a1.sum()
    b1=1/(1+np.exp(-v[1+3*n:1+4*n]))
    mu_a=np.concatenate([(1-q)*a0,q*a1]); mu_b=np.concatenate([b0,b1])
    mean=mu_a@mu_b
    Dm=mu_a@h(mu_b)
    iid=mu_a@h(np.outer(mu_b,mu_b))@mu_a
    def comp(a,b):
        f=fid(b); return a@h(np.outer(b,b)+np.outer(f,f))@a
    idl=(1-q)*comp(a0,b0)+q*comp(a1,b1)
    N=W*iid+B*idl
    pen=0.0
    if mean<1-c: pen+= 1e3*(1-c-mean)
    if Dm<floor: pen+= 1e3*(floor-Dm)
    return N/max(Dm,1e-12)+pen
best={}
for natoms in [4,5]:
  for c in [0.38284,0.38288]:
    bv=np.inf
    for trial in range(600):
        v=rng.normal(0,2.5,1+4*natoms)
        r=minimize(ratio,v,args=(c,natoms,1e-3),method='Nelder-Mead',
                   options={'maxiter':20000,'maxfev':20000,'fatol':1e-14,'xatol':1e-12})
        r2=minimize(ratio,r.x,args=(c,natoms,1e-3),method='Nelder-Mead',
                   options={'maxiter':20000,'maxfev':20000,'fatol':1e-15,'xatol':1e-13})
        if r2.fun<bv: bv=r2.fun; bx=r2.x
    print("natoms=%d c=%.5f  min ratio found = %.8f"%(natoms,c,bv))
