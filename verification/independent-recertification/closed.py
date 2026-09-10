import numpy as np, sys
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from evaluator import *
from scipy.optimize import minimize_scalar

w=0.810222
def hid(y,d,q,w,c,f):
    xs0=np.array([0.0,y]); w0=np.array([1-d,d]); xs1=np.array([1.0]); w1=np.array([1.0])
    num,den,mean = pieces(xs0,w0,xs1,w1,q,w,f)
    return num/den, mean
def twopt(x,w,c,f):
    p=(1-c)/x
    if p>1: return np.inf
    fx=f(np.array([x]))[0]
    return (w*p*h(np.array([x*x]))[0] + (1-w)*p*h(np.array([x*x+fx*fx]))[0])/h(np.array([x]))[0]

for c in [0.38284, 0.38288, 0.382885260]:
    print("=== c =",c," 2w(1-c) =", 2*w*(1-c))
    r=minimize_scalar(lambda x: twopt(x,w,c,f_ideal), bounds=(0.5,0.9999),method='bounded',options={'xatol':1e-13})
    print("  two-point min ratio %.9f at x=%.7f, p=%.6f" % (r.fun,r.x,(1-c)/r.x))
    print("  two-point at x=0.6909: %.9f" % twopt(0.6909,w,c,f_ideal))
    for d in [1e-2,1e-3,1e-4,1e-5,1e-6]:
        vals=[]
        for y in [0.05,0.2,0.5,0.7,0.9]:
            v,m = hid(y,d,1-c,w,c,f_ideal); vals.append((y,v,m))
        print("  delta=%.0e :"%d, " ".join("y=%.2f r=%.9f"%(y,v) for y,v,m in vals))
# fixed point c**
def G(c):
    r=minimize_scalar(lambda x: 1-x*h(np.array([x]))[0]/(1-(1-h(np.array([x*x]))[0])/(2*(1-c))),
                      bounds=(0.5,1/np.sqrt(2)),method='bounded',options={'xatol':1e-13})
    return r.fun, r.x
c=0.3828
for _ in range(200):
    c,xstar=G(c)
print("c** = %.9f  x*=%.7f  w=%.6f" % (c,xstar,1/(2*(1-c))))
