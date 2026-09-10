import numpy as np
from mpmath import mp, mpf, log, sqrt as msqrt
mp.dps=50
def H(p):
    p=mpf(p)
    if p<=0 or p>=1: return mpf(0)
    return -(p*log(p)+(1-p)*log(1-p))/log(2)
w=mpf('0.810222'); c=mpf('0.38284'); C=mpf('1.00005'); t0=mpf('0.006')
r=(1-w)/w
Lt=lambda u: log(1/mpf(u))/log(2)+(1-mpf(u))/log(2)
Lt0=Lt(t0); ht0=H(t0); rho=(1-t0)/ht0
Phi=2/Lt0+t0*(Lt0+1+t0/log(2))/Lt0
G=(1-c)-C/(2*w); eps0=G/rho
print("r        =",mp.nstr(r,18),  " (doc 0.234229630891286586)")
print("Lt0      =",mp.nstr(Lt0,18)," (doc 8.81486065458456)")
print("h(t0)    =",mp.nstr(ht0,18)," (doc 0.052915080344847655)")
print("rho      =",mp.nstr(rho,15)," (doc 18.7848150947159)")
print("Phi(t0)  =",mp.nstr(Phi,15)," (doc 0.233576137)   Phi<=r:",Phi<=r," slack",mp.nstr(r-Phi,6))
print("2w(1-c)  =",mp.nstr(2*w*(1-c),15)," (doc 1.00007321904)")
print("G        =",mp.nstr(G,15)," (doc 1.43288135844250e-5)")
print("eps0     =",mp.nstr(eps0,12)," (doc 7.62787044e-7)   >=1e-7:",eps0>=mpf('1e-7'))
print("w_max allowed by Lemma6: 1/(1+Phi) =",mp.nstr(1/(1+Phi),12)," vs w**=0.8102220991 ->ok:",1/(1+Phi)>mpf('0.8102220991'))
