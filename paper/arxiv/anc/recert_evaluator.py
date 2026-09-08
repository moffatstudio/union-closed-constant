"""Independent evaluator of the single-letter certificate (union-closed).
Written from paper/note.tex Sections 2-4 only; no repo code consulted.
"""
import numpy as np
from scipy.optimize import minimize

LOG2 = np.log(2.0)

def h(p):
    p = np.asarray(p, dtype=float)
    p = np.clip(p, 0.0, 1.0)
    out = np.zeros_like(p)
    m = (p > 0) & (p < 1)
    pp = p[m]
    out[m] = -(pp*np.log(pp) + (1-pp)*np.log1p(-pp))/LOG2
    return out

# ---------------- kernels ----------------
def f_liu(x):
    x = np.asarray(x, float)
    return x*(1-x)

def f_ideal(x):
    x = np.asarray(x, float)
    out = np.zeros_like(x)
    a = x <= 0.5
    out[a] = np.minimum(x[a], 1-x[a])
    b = (x > 0.5) & (x <= 1/np.sqrt(2))
    out[b] = np.sqrt(np.maximum(0.0, 0.5 - x[b]**2))
    return out

# ---------------- objective ----------------
def pieces(xs0, w0, xs1, w1, q, w, f):
    """Return (numerator, denominator) of the certificate ratio."""
    # mu = (1-q) P0 + q P1  as a single atom list
    mx = np.concatenate([xs0, xs1])
    mw = np.concatenate([(1-q)*w0, q*w1])
    # iid term: E_{mu (x) mu} h(XY)
    iid = mw @ h(np.outer(mx, mx)) @ mw
    # cond-iid term
    def prod_term(xs, ws):
        K = np.outer(xs, xs) + np.outer(f(xs), f(xs))
        return ws @ h(K) @ ws
    ci = (1-q)*prod_term(xs0, w0) + q*prod_term(xs1, w1)
    num = w*iid + (1-w)*ci
    den = mw @ h(mx)
    mean = mw @ mx
    return num, den, mean

def ratio(xs0, w0, xs1, w1, q, w, f):
    num, den, mean = pieces(xs0, w0, xs1, w1, q, w, f)
    return num/den

# ---------------- parametrisation ----------------
def unpack(z, n):
    xs0 = z[0:n]; l0 = z[n:2*n]; xs1 = z[2*n:3*n]; l1 = z[3*n:4*n]; q = z[4*n]
    def sm(l):
        e = np.exp(l - l.max()); return e/e.sum()
    return xs0, sm(l0), xs1, sm(l1), q

def make_funs(n, w, f, c, hfloor=1e-3):
    def obj(z):
        xs0, w0, xs1, w1, q = unpack(z, n)
        num, den, mean = pieces(xs0, w0, xs1, w1, q, w, f)
        return num/max(den, 1e-15)
    def con_mean(z):
        xs0, w0, xs1, w1, q = unpack(z, n)
        _, _, mean = pieces(xs0, w0, xs1, w1, q, w, f)
        return mean - (1-c)
    def con_h(z):
        xs0, w0, xs1, w1, q = unpack(z, n)
        _, den, _ = pieces(xs0, w0, xs1, w1, q, w, f)
        return den - hfloor
    return obj, con_mean, con_h

def local_min(z0, n, w, f, c, hfloor=1e-3):
    obj, cm, ch = make_funs(n, w, f, c, hfloor)
    bnds = [(0.0,1.0)]*n + [(-15,15)]*n + [(0.0,1.0)]*n + [(-15,15)]*n + [(0.0,1.0)]
    cons = [{'type':'ineq','fun':cm}, {'type':'ineq','fun':ch}]
    r = minimize(obj, z0, method='SLSQP', bounds=bnds, constraints=cons,
                 options={'maxiter':500,'ftol':1e-14})
    z = r.x
    if cm(z) < -1e-9 or ch(z) < -1e-9:
        return np.inf, z
    return obj(z), z

def describe(z, n):
    xs0, w0, xs1, w1, q = unpack(z, n)
    def law(xs, ws):
        idx = np.argsort(-ws)
        return [(round(float(xs[i]),6), round(float(ws[i]),6)) for i in idx if ws[i] > 1e-6]
    return {'q': float(q), 'P0': law(xs0, w0), 'P1': law(xs1, w1)}
