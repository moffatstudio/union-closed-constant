import numpy as np
from math import sqrt
def h(p):
    p=np.asarray(p,float); o=np.zeros_like(p); m=(p>0)&(p<1)
    o[m]=-p[m]*np.log2(p[m])-(1-p[m])*np.log2(1-p[m]); return o
def two_point(x,p,w,f):
    # mu = p d_x + (1-p) d_0 ; iid term + kernel term (q=0, single component)
    iid = p*p*h(np.array([x*x]))[0]
    ker = p*p*h(np.array([x*x+f(x)**2]))[0]
    return (w*iid+(1-w)*ker)/(p*h(np.array([x]))[0])
fliu=lambda x: x*(1-x)
p,x,beta,cp=0.893604513905457,0.690787593924988,0.100052559862974,0.382709087918741
print("mean check 1-p*x =",1-p*x, " vs c'=",cp)
print("Liu ratio at his point:",two_point(x,p,1-beta,fliu))
# and the minimum over x at his w,c
import scipy.optimize as so
def rat(xx,c,w,f):
    pp=(1-c)/xx
    if pp>1: return np.inf
    return two_point(xx,pp,w,f)
xs=np.linspace(0.4,0.999,400000)
v=[rat(t,cp,1-beta,fliu) for t in xs]; i=int(np.argmin(v))
print("min over x:",v[i],"at",xs[i])
