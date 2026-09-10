import numpy as np
from math import sqrt
from scipy.optimize import minimize
rng=np.random.default_rng(7)
def h(p):
    p=np.asarray(p,float); o=np.zeros_like(p); m=(p>1e-300)&(p<1-1e-16)
    o[m]=-p[m]*np.log2(p[m])-(1-p[m])*np.log2(1-p[m]); return o
def fid(x):
    x=np.asarray(x,float)
    return np.where(x<=0.5,x,np.where(x<=1/sqrt(2),np.sqrt(np.maximum(0.5-x*x,0.0)),0.0))
W=0.810222099; B=1-W
def unpack(v,n):
    q=1/(1+np.exp(-v[0]))
    a0=np.exp(v[1:1+n]-v[1:1+n].max()); a0/=a0.sum()
    b0=1/(1+np.exp(-v[1+n:1+2*n]))
    a1=np.exp(v[1+2*n:1+3*n]-v[1+2*n:1+3*n].max()); a1/=a1.sum()
    b1=1/(1+np.exp(-v[1+3*n:1+4*n]))
    return q,a0,b0,a1,b1
def obj(v,c,n,floor):
    q,a0,b0,a1,b1=unpack(v,n)
    ma=np.concatenate([(1-q)*a0,q*a1]); mb=np.concatenate([b0,b1])
    mean=ma@mb; D=ma@h(mb)
    iid=ma@h(np.outer(mb,mb))@ma
    def comp(a,b):
        f=fid(b); return a@h(np.outer(b,b)+np.outer(f,f))@a
    N=W*iid+B*((1-q)*comp(a0,b0)+q*comp(a1,b1))
    r=N/max(D,1e-14)
    pen=1e3*max(0,1-c-mean)+1e3*max(0,floor-D)
    return r+pen
for n in [4,5]:
  for c in [0.38284,0.38288]:
    bv=np.inf
    for t in range(120):
        v=rng.normal(0,3.0,1+4*n)
        r=minimize(obj,v,args=(c,n,1e-3),method='Powell',options={'maxiter':6000,'ftol':1e-13,'xtol':1e-11})
        if r.fun<bv: bv=r.fun; bx=r.x
    q,a0,b0,a1,b1=unpack(bx,n)
    import sys;print("n=%d c=%.5f  min ratio = %.8f"%(n,c,bv))
    print("   q=%.4f  P0 atoms=%s w=%s"%(q,np.round(b0,4),np.round(a0,4)))
    print("   P1 atoms=%s w=%s"%(np.round(b1,4),np.round(a1,4)))
