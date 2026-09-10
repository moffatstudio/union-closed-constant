import numpy as np
from math import log2, sqrt
from scipy.optimize import brentq
def h(p):
    if p<=0 or p>=1: return 0.0
    return -p*log2(p)-(1-p)*log2(1-p)
r2=1/sqrt(2)
def thresh(c):
    w=1/(2*(1-c))
    g=lambda x: h(x)-(w*h(x*x)+1-w)   # <=0 means x in X_c
    return brentq(g,0.5,r2)
print("smallest x in X_c  (X_c = [thresh, 1/sqrt2]):")
for c in [0.2,0.3,0.38,0.382885,0.40,0.45,0.49]:
    t=thresh(c)
    print("  c=%.6f  w0=%.6f  thresh=%.6f   contains 0.62? %s"%(c,1/(2*(1-c)),t,t<=0.62))
# minimiser location over c range
def G(c):
    w=1/(2*(1-c)); best=(9,None)
    for x in np.linspace(0.5,r2,200001):
        d=w*h(x*x)+1-w
        if h(x)>d: continue
        v=1-x*h(x)/d
        if v<best[0]: best=(v,x)
    return best
for c in [0.2,0.45]:
    v,x=G(c); print("c=%.2f  G=%.9f minimiser x=%.5f"%(c,v,x))
# is c<=G(c) outside [0.2,0.45]?
for c in [0.05,0.15,0.2,0.45,0.46,0.49]:
    v,x=G(c); print("c=%.3f  G(c)=%.9f  c<=G(c)? %s"%(c,v,c<=v))
