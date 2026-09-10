import numpy as np
np.seterr(all='ignore')
def h(p):
    p=np.asarray(p,float); o=np.zeros_like(p); m=(p>0)&(p<1)
    o[m]=-(p[m]*np.log2(p[m])+(1-p[m])*np.log2(1-p[m])); return o
w=0.810222; t0=0.006
g=np.logspace(-16,np.log10(t0),1600)
T,Tp=np.meshgrid(g,g)
tau=T+Tp-T*Tp; A=T*(1-Tp); B=Tp*(1-T); gam=T*Tp/tau; alp=A/(A+B)
Lam_stable=tau*h(gam)+(A+B)*h(alp)          # exact identity, numerically stable
Lam_naive=h(T)+h(Tp)-h((1-T)*(1-Tp))
den=(1-w)*np.sqrt(h(T)*h(Tp))
for name,L in [("naive",Lam_naive),("stable",Lam_stable)]:
    R=w*L/den; i=np.unravel_index(np.nanargmax(R),R.shape)
    print("%-7s max ratio=%.6f at t=%.3e t'=%.3e"%(name,np.nanmax(R),T[i],Tp[i]))
# confirm with mpmath at the naive argmax and at the corner
from mpmath import mp, mpf, log, sqrt
mp.dps=60
def H(p):
    p=mpf(p)
    if p<=0 or p>=1: return mpf(0)
    return -(p*log(p)+(1-p)*log(1-p))/log(2)
def Lam_mp(t,tp):
    t=mpf(t); tp=mpf(tp); tau=t+tp-t*tp; A=t*(1-tp); B=tp*(1-t)
    return tau*H(t*tp/tau)+(A+B)*H(A/(A+B))
W=mpf('0.810222')
for t,tp in [(1e-16,1e-16),(1e-16,0.006),(1e-10,1e-10),(1e-6,1e-6),(0.006,0.006),(0.003,0.006),(1e-13,1e-4)]:
    R=W*Lam_mp(t,tp)/((1-W)*sqrt(H(t)*H(tp)))
    print("  mpmath t=%.0e t'=%.0e   ratio=%s"%(t,tp,mp.nstr(R,10)))
