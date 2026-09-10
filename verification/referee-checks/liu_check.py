import numpy as np
from math import log2, sqrt
from scipy.optimize import brentq, minimize_scalar
def h(p):
    if p<=0 or p>=1: return 0.0
    return -p*log2(p)-(1-p)*log2(1-p)
# Liu kernel diagonal
for x in [0.5,0.6,0.69,0.6908,0.75,0.8,0.9]:
    d=x*x+x*x*(1-x)**2
    print("x=%.4f diag=%.6f  1-x^2=%.6f  h(diag)=%.6f h(x^2)=%.6f"%(x,d,1-x*x,h(d),h(x*x)))
f=lambda x: x*x+x*x*(1-x)**2-(1-x*x)
print("neutral point:", brentq(f,0.5,0.9))
# (D) at w=0.9
def Dbound(x,w): return 1 - x*h(x)/(w*h(x*x)+(1-w))
r=minimize_scalar(lambda x: Dbound(x,0.9), bounds=(0.5,1/sqrt(2)),method='bounded')
print("D bound at w=0.9:", r.fun, "at x=",r.x)
# ideal f
def fid(x):
    if x<=0.5: return x
    if x<=1/sqrt(2): return sqrt(0.5-x*x)
    return 0.0
def ratio_twopoint(x,c,w):
    p=(1-c)/x
    if p>1: return np.inf
    d=x*x+fid(x)**2
    return p*(w*h(x*x)+(1-w)*h(d))/h(x)
for c in [0.38284,0.38288,0.382885260]:
    w=0.810222099
    xs=np.linspace(1e-4,0.9999,200000)
    vals=[ratio_twopoint(x,c,w) for x in xs]
    i=int(np.argmin(vals)); print("c=%.8f  min two-point ratio=%.8f at x=%.6f"%(c,vals[i],xs[i]))
