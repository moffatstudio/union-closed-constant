"""
General conditionally-iid protocols for the union-closed entropy method (lead, 2026-09-08).

Protocol: given shared uniform U and conditional zero-probabilities x (for A) and y (for B), the two bits are
generated conditionally independently given U with P(A_i=0 | U=u) = r_x(u), r_x in [0,1], int r_x = x.
Then P(A_i=0, B_i=0 | prefixes) = x*y + K(x,y),  K(x,y) = Cov(r_x, r_y)  -- a realizable PSD kernel.
Liu (2306.08824) used K(x,y) = f(x) f(y), f(x) = x(1-x).

Adversary (Liu Thm 9, valid for ANY conditionally-iid protocol): the joint law of the two prefix zero-probabilities
is a mixture of two products  P_XY = (1-q) P0 (x) P0 + q P1 (x) P1,  marginal mu = (1-q) P0 + q P1,  E_mu[X] >= 1 - c.
Certificate for constant c:   min over adversary of
    R = [ (1-beta) E_{mu(x)mu} h(XY) + beta E_{P_XY} h(XY + K(X,Y)) ] / E_mu h(X)   >= 1.
(beta = weight on the K-protocol, 1-beta on the plain iid protocol.)
Here we allow P0, P1 each m atoms with free weights (more general than Liu's shared-weight 3-atom form).
"""
import numpy as np
from scipy.optimize import minimize

def h(x):
    x = np.clip(x, 1e-300, 1 - 1e-16)
    return -x*np.log(x) - (1-x)*np.log(1-x)

# ---------------- kernels ----------------
def K_liu(x, y):
    return np.outer(x*(1-x), y*(1-y))

def make_rank_kernel(fs):
    """fs: list of callables f_j; K = sum_j f_j(x) f_j(y). Realizable iff sum_j |f_j(x)| <= min(x,1-x)."""
    def K(x, y):
        return sum(np.outer(f(x), f(y)) for f in fs)
    return K

def make_interval_kernel(a):
    """r_x = indicator of [a(x), a(x)+x]; K(x,y) = |I_x cap I_y| - xy. Realizable iff 0 <= a(x) <= 1-x."""
    def K(x, y):
        ax, ay = a(x), a(y)
        lo = np.maximum.outer(ax, ay); hi = np.minimum.outer(ax + x, ay + y)
        return np.maximum(hi - lo, 0.0) - np.outer(x, y)
    return K

# ---------------- adversary ----------------
def unpack(z, m):
    # z = [q, w0 (m), x0 (m), w1 (m), x1 (m)]  weights via softmax-free normalisation: use raw then normalise
    q = z[0]
    w0 = np.abs(z[1:1+m]); w0 = w0/ w0.sum() if w0.sum() > 0 else np.ones(m)/m
    x0 = z[1+m:1+2*m]
    w1 = np.abs(z[1+2*m:1+3*m]); w1 = w1/ w1.sum() if w1.sum() > 0 else np.ones(m)/m
    x1 = z[1+3*m:1+4*m]
    return q, w0, x0, w1, x1

def ratio(z, m, K, beta):
    q, w0, x0, w1, x1 = unpack(z, m)
    atoms = np.concatenate([x0, x1]); wts = np.concatenate([(1-q)*w0, q*w1])
    e_iid = wts @ h(np.outer(atoms, atoms)) @ wts
    e_K = (1-q) * (w0 @ h(np.outer(x0, x0) + K(x0, x0)) @ w0) + q * (w1 @ h(np.outer(x1, x1) + K(x1, x1)) @ w1)
    e_h = wts @ h(atoms)
    if e_h < 1e-12: return 10.0
    return ((1-beta)*e_iid + beta*e_K) / e_h

def mean_x(z, m):
    q, w0, x0, w1, x1 = unpack(z, m)
    return (1-q)*(w0 @ x0) + q*(w1 @ x1)

def adversary_min(K, beta, c, m=3, restarts=60, seed=0, inits=None):
    rng = np.random.default_rng(seed)
    bounds = [(0,1)]*(1+4*m)
    cons = [{"type": "ineq", "fun": lambda z: mean_x(z, m) - (1-c)}]
    best = (np.inf, None)
    starts = []
    if inits is not None: starts += list(inits)
    starts += structured_inits(m, rng)
    for _ in range(restarts): starts.append(rng.random(1+4*m))
    for z0 in starts:
        try:
            r = minimize(ratio, z0, args=(m, K, beta), method="SLSQP", bounds=bounds, constraints=cons,
                         options={"maxiter": 400, "ftol": 1e-13})
        except Exception:
            continue
        if mean_x(r.x, m) < (1-c) - 1e-9: continue
        if r.fun < best[0]: best = (r.fun, r.x)
    return best

def c_max(K, beta, m=3, restarts=40, lo=0.375, hi=0.40, tol=2e-6, seed=0, verbose=False):
    """Largest c with min ratio >= 1 (bisection). Returns (c, worst adversary at c)."""
    last = None
    while hi - lo > tol:
        mid = 0.5*(lo+hi)
        val, z = adversary_min(K, beta, mid, m=m, restarts=restarts, seed=seed, inits=[last] if last is not None else None)
        if verbose: print("   c=%.6f min ratio=%.7f" % (mid, val), flush=True)
        if val >= 1.0 - 1e-9: lo = mid
        else: hi = mid; last = z
    return lo, last

def describe(z, m):
    q, w0, x0, w1, x1 = unpack(z, m)
    return "q=%.4f | P0: %s | P1: %s" % (q, list(zip(np.round(x0,4), np.round(w0,4))), list(zip(np.round(x1,4), np.round(w1,4))))

if __name__ == "__main__":
    import sys, time
    t0 = time.time()
    # 1. reproduce Liu: c'=0.382709087918741, beta*=0.100052559862974 -> min ratio should be ~1
    val, z = adversary_min(K_liu, 0.100052559862974, 0.382709087918741, m=3, restarts=150)
    print("Liu kernel at his (c,beta): min ratio = %.9f   adversary: %s" % (val, describe(z, 3)))
    val, z = adversary_min(K_liu, 0.100052559862974, 0.3830, m=3, restarts=150)
    print("Liu kernel at c=0.3830: min ratio = %.9f   adversary: %s" % (val, describe(z, 3)))
    print("time", time.time()-t0)

# ---------- K_new: comonotone indicator for x<=1/2, ideal-variance step function for x in [1/2,1/sqrt2], constant beyond ----------
def _r_params(x):
    """r_x(u) = 1 for u<=t, = lam for u>t (x in [1/2, 1/sqrt2]); lam=(2x-1)/(2(1-x)), t = 1-(1-x)/(1-lam)."""
    lam = (2*x - 1) / (2*(1 - x)); t = 1 - (1 - x) / (1 - lam)
    return t, lam
def _Err(x, y):
    """E[r_x r_y] for the piecewise family (vectorised over outer product)."""
    x = np.asarray(x, float); y = np.asarray(y, float)
    X, Y = np.meshgrid(x, y, indexing='ij')
    out = X * Y  # default: independent (K=0), covers any pair involving x>=1/sqrt2
    # regimes
    S = X <= 0.5; M = (X > 0.5) & (X < 1/np.sqrt(2))
    S2 = Y <= 0.5; M2 = (Y > 0.5) & (Y < 1/np.sqrt(2))
    # small-small: min(x,y)
    out = np.where(S & S2, np.minimum(X, Y), out)
    # small-mid: E[1_{u<=y} r_x] = y if y <= t(x) else t + (y-t)*lam  (y small, x mid)
    tX, lX = _r_params(np.clip(X, 0.5001, 0.7070)); tY, lY = _r_params(np.clip(Y, 0.5001, 0.7070))
    sm = np.where(Y <= tX, Y, tX + (Y - tX) * lX)
    out = np.where(S2 & M, sm, out)
    ms = np.where(X <= tY, X, tY + (X - tY) * lY)
    out = np.where(S & M2, ms, out)
    # mid-mid: with t1<=t2: t1 + (t2-t1)*lam1 + (1-t2)*lam1*lam2
    t1 = np.minimum(tX, tY); t2 = np.maximum(tX, tY)
    l1 = np.where(tX <= tY, lX, lY); l2 = np.where(tX <= tY, lY, lX)
    mm = t1 + (t2 - t1) * l1 + (1 - t2) * l1 * l2
    out = np.where(M & M2, mm, out)
    return out
def K_new(x, y):
    x = np.asarray(x, float); y = np.asarray(y, float)
    return _Err(x, y) - np.outer(x, y)

def structured_inits(m, rng, n=12):
    """Adversary warm starts: degenerate (eps,1) mixtures, two-point (x*,0) laws, Liu/Cambie-like laws."""
    S = []
    for q in (0.55, 0.62, 0.7):
        for eps in (1e-4, 1e-3, 1e-2):
            z = np.zeros(1+4*m); z[0] = q; z[1:1+m] = 1.0/m; z[1+m:1+2*m] = eps; z[1+2*m:1+3*m] = 1.0/m; z[1+3*m:1+4*m] = 1.0
            S.append(z)
    for xs in np.linspace(0.6, 0.75, 7):
        z = np.zeros(1+4*m); z[0] = 0.0; z[1:1+m] = 0.0; z[1] = 0.89; z[2] = 0.11; z[1+m:1+2*m] = 0.0; z[1+m] = xs
        z[1+2*m:1+3*m] = 1.0/m; z[1+3*m:1+4*m] = rng.random(m); S.append(z)
    z = np.zeros(1+4*m); z[0]=0.0; z[1]=0.921; z[2]=0.079; z[1+m]=0.6705; z[2+m]=1.0; z[1+2*m:1+3*m]=1/m; z[1+3*m:1+4*m]=rng.random(m); S.append(z)
    return S
