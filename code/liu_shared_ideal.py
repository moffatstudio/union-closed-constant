"""
Cross-check (task 2): Liu's SHARED-WEIGHT parametrisation of the adversary (P0 and P1 share
the same m weights a1..am; only the atom POSITIONS differ between P0 and P1 -- see
liu_reproduce.py's reproduce_B, which hard-codes this for m=3 and K_liu), generalised here to
an arbitrary kernel K and m=3, so we can cross-check kernel_game.py's more general
independent-weight adversary_min against this more constrained (Liu's original) family.

If the shared-weight family's optimum matches kernel_game.py's free-weight optimum (same
min ratio, same c_max), that's evidence the free-weight optimum genuinely wants shared
weights (i.e. is not an artifact of the more general parametrisation), consistent with Liu's
own reduction argument.

Objective (natural log, matches frankl5.m / liu_reproduce.py):
  R = [(1-beta) E_{mu x mu} h(XY) + beta * ( qbar * E_{P0 x P0} h(XY+K(X,Y)) + q * E_{P1 x P1} h(XY+K(X,Y)) )] / E_mu h(X)
  mu = qbar*P0 + q*P1,  P0,P1 share weights w (m-dim simplex), differ only in atom positions.
"""
import sys, time
import numpy as np
from scipy.optimize import minimize
from kernel_game import h, make_rank_kernel

def f_ideal(x):
    x = np.asarray(x, float)
    return np.where(x <= 0.5, np.minimum(x, 1 - x), np.sqrt(np.maximum(0.0, 0.5 - x**2)))

def f_liu(x): return x * (1 - x)

KERNELS = {"liu": make_rank_kernel([f_liu]), "ideal": make_rank_kernel([f_ideal])}

def unpack(z, m):
    q = z[0]
    w = np.abs(z[1:1+m]); w = w / w.sum() if w.sum() > 0 else np.ones(m) / m
    x0 = z[1+m:1+2*m]
    x1 = z[1+2*m:1+3*m]
    return q, w, x0, x1

def ratio(z, m, K, beta):
    q, w, x0, x1 = unpack(z, m)
    qb = 1 - q
    atoms = np.concatenate([x0, x1]); wts = np.concatenate([qb * w, q * w])
    e_iid = wts @ h(np.outer(atoms, atoms)) @ wts
    e_K = qb * (w @ h(np.outer(x0, x0) + K(x0, x0)) @ w) + q * (w @ h(np.outer(x1, x1) + K(x1, x1)) @ w)
    e_h = wts @ h(atoms)
    if e_h < 1e-12: return 10.0
    return ((1 - beta) * e_iid + beta * e_K) / e_h

def mean_x(z, m):
    q, w, x0, x1 = unpack(z, m)
    return (1 - q) * (w @ x0) + q * (w @ x1)

def adversary_min_shared(K, beta, c, m=3, restarts=200, seed=0, inits=None):
    rng = np.random.default_rng(seed)
    bounds = [(0, 1)] * (1 + 2*m + m)  # q, w(m), x0(m), x1(m) -- note dim = 1+m+m+m = 1+3m
    bounds = [(0, 1)] * (1 + 3*m)
    cons = [{"type": "ineq", "fun": lambda z: mean_x(z, m) - (1 - c)}]
    best = (np.inf, None)
    starts = list(inits) if inits is not None else []
    for _ in range(restarts): starts.append(rng.random(1 + 3*m))
    for z0 in starts:
        try:
            r = minimize(ratio, z0, args=(m, K, beta), method="SLSQP", bounds=bounds,
                         constraints=cons, options={"maxiter": 400, "ftol": 1e-13})
        except Exception:
            continue
        if mean_x(r.x, m) < (1 - c) - 1e-9: continue
        if r.fun < best[0]: best = (r.fun, r.x)
    return best

def describe(z, m):
    q, w, x0, x1 = unpack(z, m)
    return "q=%.4f | shared w=%s | P0 atoms=%s | P1 atoms=%s" % (
        q, list(np.round(w, 4)), list(np.round(x0, 4)), list(np.round(x1, 4)))

def c_max_shared(K, beta, m=3, restarts=60, lo=0.375, hi=0.40, tol=2e-6, seed=0, verbose=False):
    last = None
    while hi - lo > tol:
        mid = 0.5 * (lo + hi)
        val, z = adversary_min_shared(K, beta, mid, m=m, restarts=restarts, seed=seed,
                                       inits=[last] if last is not None else None)
        if verbose: print("   c=%.6f min ratio=%.7f" % (mid, val), flush=True)
        if val >= 1.0 - 1e-9: lo = mid
        else: hi = mid; last = z
    return lo, last

if __name__ == "__main__":
    name = sys.argv[1] if len(sys.argv) > 1 else "ideal"
    beta = float(sys.argv[2]) if len(sys.argv) > 2 else 0.15
    m = int(sys.argv[3]) if len(sys.argv) > 3 else 3
    restarts = int(sys.argv[4]) if len(sys.argv) > 4 else 200
    K = KERNELS[name]
    t0 = time.time()
    # sanity check against liu_reproduce.py's known answer
    if name == "liu":
        val, z = adversary_min_shared(K, 0.100052559862974, 0.382709087918741, m=3, restarts=restarts, seed=1)
        print("SANITY liu shared-weight at Liu's own (c,beta): min ratio=%.9f  %s" % (val, describe(z, 3)))
    c, z = c_max_shared(K, beta, m=m, restarts=restarts, verbose=True)
    print("SHARED-WEIGHT kernel=%s beta=%.3f m=%d : c_max=%.6f  adversary: %s  (%.0fs)" %
          (name, beta, m, c, describe(z, m) if z is not None else None, time.time() - t0), flush=True)
