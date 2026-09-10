import numpy as np
from math import log2, sqrt
from scipy.optimize import minimize_scalar, brentq
def h(p):
    if p<=0 or p>=1: return 0.0
    return -p*log2(p)-(1-p)*log2(1-p)
w=0.810222; c=0.38284
# 1. where does p=h(x)/(w h(x^2)+1-w) exceed 1 on [1/2,1/sqrt2]?
def p_of(x): return h(x)/(w*h(x*x)+1-w)
for x in [0.5,0.55,0.6,0.617,0.65,0.6909,0.7071]:
    print("x=%.4f p=%.5f  Dbound=%.7f"%(x,p_of(x),1-x*h(x)/(w*h(x*x)+1-w)))
print("p=1 at x =", brentq(lambda x: p_of(x)-1, 0.5,0.7071))
# 2. Claim 1 sub-case
for eta in [0.25,0.1,0.01]:
    print("eta=%.2f h(1/2-eta/2)=%.6f  1-eta=%.4f  ok=%s"%(eta,h(0.5-eta/2),1-eta,h(0.5-eta/2)>=1-eta))
# 3. appendix constants
xs=0.690908
print("h(x**)=%.6f h(x**^2)=%.6f"%(h(xs),h(xs*xs)))
def c2(ww): 
    r=minimize_scalar(lambda x:1-x*h(x)/(ww*h(x*x)+1-ww),bounds=(0.5,1/sqrt(2)),method='bounded',options={'xatol':1e-13})
    return r.fun,r.x
for ww in [0.899947,0.85,0.810222]:
    v,xx=c2(ww); print("c2(%.6f)=%.6f at x=%.4f"%(ww,v,xx))
print("(H) at c=0.38284: w>=",1/(2*(1-0.38284)))
