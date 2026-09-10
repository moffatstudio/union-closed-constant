import numpy as np
from math import log2, sqrt
def h(p):
    if p<=0 or p>=1: return 0.0
    return -p*log2(p)-(1-p)*log2(1-p)
w=0.810222; c=0.38284
def kappa(eta): return (1-eta)*(1-2/log2(1/eta))
def B(eta,E): return 2*w*kappa(eta)*(1-c-eta-E/h(eta))
print("paper's instance eta=1e-4, E=1e-7 :", B(1e-4,1e-7))
print("kappa(1e-4)=",kappa(1e-4), " h(1e-4)=",h(1e-4))
for E in [1e-7,1e-12,1e-30,1e-100]:
    best=-9; be=None
    for k in range(3,4000):
        eta=2.0**(-k/10)
        if eta<=0: break
        v=B(eta,E)
        if v>best: best,be=v,eta
    print("E=%.0e  max_eta B = %.8f  at eta=%.3e   (2w(1-c)=%.8f)"%(E,best,be,2*w*(1-c)))
