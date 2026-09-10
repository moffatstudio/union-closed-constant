import numpy as np
from math import log2, sqrt
from scipy.optimize import brentq
def h(p):
    if p<=0 or p>=1: return 0.0
    return -p*log2(p)-(1-p)*log2(1-p)
# 1. G with restricted domain X_c : monotone? unique root?
def G(c,restrict=True,n=400001):
    xs=np.linspace(0.5,1/sqrt(2),n); w0=1/(2*(1-c)); best=np.inf; bx=None
    for x in xs:
        den=w0*h(x*x)+1-w0
        if restrict and h(x)>den: continue
        v=1-x*h(x)/den
        if v<best: best,bx=v,x
    return best,bx
for c in [0.20,0.30,0.36,0.38,0.3828,0.382885,0.39,0.42,0.45]:
    gr,xr=G(c,True); gu,xu=G(c,False)
    print("c=%.6f  G_restricted=%.9f (x=%.5f)  G_unrestricted=%.9f (x=%.5f)  same=%s"%(c,gr,xr,gu,xu,abs(gr-gu)<1e-12))
print()
f=lambda c: G(c,True)[0]-c
print("root of c=G(c) restricted:", brentq(f,0.30,0.40,xtol=1e-13))
# 2. hiding limit vs two-point value at c=0.38284, w as printed (0.810222) and exact
def fid(x):
    return x if x<=0.5 else (sqrt(0.5-x*x) if x<=1/sqrt(2) else 0.0)
def twopt(c,w):
    best=np.inf
    for x in np.linspace(0.6,0.72,240001):
        p=(1-c)/x
        if p>1: continue
        v=p*(w*h(x*x)+(1-w)*h(x*x+fid(x)**2))/h(x)
        best=min(best,v)
    return best
for w in [0.810222, 0.8102220991]:
    c=0.38284
    print("w=%.10f  hiding limit 2w(1-c)=%.10f   two-point min=%.10f   hiding<twopoint: %s"%(
        w,2*w*(1-c),twopt(c,w),2*w*(1-c)<twopt(c,w)))
# 3. h(lam) <= 2 sqrt(lam(1-lam)) ?
bad=[l for l in np.linspace(1e-6,1-1e-6,200000) if h(l)>2*sqrt(l*(1-l))+1e-15]
print("counterexamples to h(lam)<=2sqrt(lam(1-lam)):",len(bad))
