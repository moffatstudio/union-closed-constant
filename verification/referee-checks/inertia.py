import numpy as np
from math import sqrt
def h(p):
    p=np.asarray(p,float); out=np.zeros_like(p)
    m=(p>0)&(p<1); out[m]=-p[m]*np.log2(p[m])-(1-p[m])*np.log2(1-p[m]); return out
def fid(x):
    x=np.asarray(x,float)
    return np.where(x<=0.5,x,np.where(x<=1/sqrt(2),np.sqrt(np.maximum(0.5-x*x,0)),0.0))
def inertia(kernelfun,n,lo=0.0,hi=1.0,constraints=('one','mean')):
    x=np.linspace(lo,hi,n)
    Wt=np.ones(n)/n
    K=kernelfun(x)
    # quadratic form  nu^T K nu  with nu = W*v  (density weights). Use symmetric scaling
    A=np.sqrt(Wt)[:,None]*K*np.sqrt(Wt)[None,:]
    C=[]
    if 'one' in constraints: C.append(np.sqrt(Wt))
    if 'mean' in constraints: C.append(x*np.sqrt(Wt))
    C=np.array(C).T
    Qb,_=np.linalg.qr(C)
    P=np.eye(n)-Qb@Qb.T
    B=P@A@P
    ev=np.linalg.eigvalsh(B)
    return ev
for n in [200,400,800,1600]:
    ev=inertia(lambda x: h(np.outer(x,x)), n)
    pos=ev[ev>1e-11]
    print("iid kernel h(xy)  n=%d  #eig>1e-11: %d  top3: %s  (want 0 positive => concave)"%(n,len(pos),np.round(ev[-3:],8)))
print()
def K2(x):
    f=fid(x); return h(np.outer(x,x)+np.outer(f,f))
for n in [200,400,800,1600,3200]:
    ev=inertia(K2,n)
    print("ideal kernel n=%d  top6 eigenvalues: %s"%(n,np.round(ev[-6:],9)))

print("\n--- precise counts (positive eigenvalues of the h-form on slice) ---")
for n in [200,400,800,1600,3200]:
    ev=inertia(K2,n)
    tol=1e-12
    print("n=%d  #pos>1e-12: %d  #pos>1e-9: %d  top5: %s  min: %.3e"%(
        n,(ev>tol).sum(),(ev>1e-9).sum(),["%.4e"%v for v in ev[-5:]],ev[0]))
for n in [400,1600]:
    ev=inertia(lambda x: h(np.outer(x,x)), n)
    print("iid n=%d #pos>1e-12: %d top3: %s"%(n,(ev>1e-12).sum(),["%.3e"%v for v in ev[-3:]]))
