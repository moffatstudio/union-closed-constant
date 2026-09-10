import numpy as np
from math import log2, sqrt
def h(p):
    p=np.asarray(p,dtype=float)
    out=np.zeros_like(p)
    m=(p>0)&(p<1)
    out[m]=-p[m]*np.log2(p[m])-(1-p[m])*np.log2(1-p[m])
    return out
def h1(p):
    if p<=0 or p>=1: return 0.0
    return -p*log2(p)-(1-p)*log2(1-p)

xs=1/sqrt(2)
print("h(1/sqrt2)=",repr(h1(xs)))
print("c_ceil = 1 - h/sqrt2 =",repr(1-h1(xs)/sqrt(2)))
