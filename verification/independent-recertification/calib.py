import numpy as np, sys
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from evaluator import *

w = 0.899947; c = 0.382709087918741
# Liu's stated minimiser, exact evaluation
xs0 = np.array([0.6908, 0.0]); w0 = np.array([0.8936, 0.1064])
xs1 = np.array([0.5, 0.5]); w1 = np.array([0.5, 0.5])
print("Liu minimiser as given:", ratio(xs0,w0,xs1,w1,0.0,w,f_liu))
n,d,m = pieces(xs0,w0,xs1,w1,0.0,w,f_liu); print("  mean=",m," (need >=",1-c,")")

# optimise the two-point family exactly: mu = p d_x + (1-p) d_0, p=(1-c)/x
from scipy.optimize import minimize_scalar
def two_point(x, w, c, f):
    p = (1-c)/x
    if p > 1: return np.inf
    fx = f(np.array([x]))[0]
    num = w*p*p*h(np.array([x*x]))[0] + (1-w)*p*p*h(np.array([x*x+fx*fx]))[0]
    return num/(p*h(np.array([x]))[0])
r = minimize_scalar(lambda x: two_point(x,w,c,f_liu), bounds=(0.5,0.999), method='bounded',
                    options={'xatol':1e-12})
print("Liu two-point family min: ratio=%.10f at x=%.8f, p=%.6f" % (r.fun, r.x, (1-c)/r.x))
