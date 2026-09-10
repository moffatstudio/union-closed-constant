import numpy as np
from math import log2, sqrt
from scipy.optimize import brentq, minimize_scalar
def h(p):
    if p<=0 or p>=1: return 0.0
    return -p*log2(p)-(1-p)*log2(1-p)
def Dbound(x,w):
    den = w*h(x*x)+(1-w)
    return 1 - x*h(x)/den
def G(c, lo=0.5):
    w = 1/(2*(1-c))
    f = lambda x: Dbound(x,w)
    r = minimize_scalar(f, bounds=(lo,1/sqrt(2)), method='bounded',
                        options={'xatol':1e-14})
    return r.fun, r.x, w
for lo,name in [(0.5,'x>=1/2'),(None,'x>=1-c')]:
    def F(c):
        l = lo if lo is not None else 1-c
        return G(c,l)[0]-c
    cs = brentq(F, 0.30, 0.40, xtol=1e-15, rtol=8.9e-16)
    l = lo if lo is not None else 1-cs
    val,xstar,w = G(cs,l)
    print(name, "c**=%.12f  w=%.9f  x*=%.9f"%(cs,w,xstar))
# monotonicity of G
for c in [0.36,0.38,0.3828,0.39]:
    print("c=",c,"G=",G(c)[0])
