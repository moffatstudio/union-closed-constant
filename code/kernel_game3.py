"""
Three-protocol certificate (Liu eq. (29) with a general conditionally-iid kernel):
   w1 * E_{mu x mu} h(XY)                                      [iid, class C1 = {mu x mu}]
 + w2 * min_{W in C2(mu)} E_W h(PiSawin(X,Y))                  [Sawin max-entropy/anti-correlated; C2 = all symmetric couplings]
 + w3 * E_{P3} h(XY + K(X,Y)),  P3 = (1-q)P0xP0 + qP1xP1       [conditionally iid; C3 = mixtures of products]
 >= E_mu h(X),   for all mu = (1-q)P0 + qP1 with E[X] >= 1-c.
X,Y are zero-probabilities (x = 1-s).  PiSawin(0,0) = 1 - max(s, t, min(s+t, 1/2)) with s=1-x, t=1-y.
For fixed atoms the C2 minimisation is a transportation LP (symmetric coupling with margins mu minimising a linear objective);
we solve the (non-symmetrised) transportation LP -- its optimum can be symmetrised without changing the value.
"""
import numpy as np
from scipy.optimize import minimize, linprog
from kernel_game import h, unpack, mean_x, describe

def pi_sawin(x, y):
    s = 1 - x[:, None]; t = 1 - y[None, :]
    return 1 - np.maximum(np.maximum(s, t), np.minimum(s + t, 0.5))

def c2_min(atoms, wts):
    """min over couplings W (margins wts) of sum W_ij h(pi_sawin(x_i,x_j))."""
    n = len(atoms)
    cost = h(pi_sawin(atoms, atoms)).ravel()
    A_eq = np.zeros((2*n, n*n)); b_eq = np.concatenate([wts, wts])
    for i in range(n):
        A_eq[i, i*n:(i+1)*n] = 1.0          # row sums
        A_eq[n+i, i::n] = 1.0               # column sums
    res = linprog(cost, A_eq=A_eq, b_eq=b_eq, bounds=(0, None), method="highs")
    return res.fun if res.success else np.inf

def ratio3(z, m, K, w):
    w1, w2, w3 = w
    q, w0, x0, w1v, x1 = unpack(z, m)
    atoms = np.concatenate([x0, x1]); wts = np.concatenate([(1-q)*w0, q*w1v])
    e_h = wts @ h(atoms)
    if e_h < 1e-12: return 10.0
    tot = 0.0
    if w1 > 0: tot += w1 * (wts @ h(np.outer(atoms, atoms)) @ wts)
    if w2 > 0: tot += w2 * c2_min(atoms, wts)
    if w3 > 0: tot += w3 * ((1-q) * (w0 @ h(np.outer(x0, x0) + K(x0, x0)) @ w0) + q * (w1v @ h(np.outer(x1, x1) + K(x1, x1)) @ w1v))
    return tot / e_h

def adversary_min3(K, w, c, m=3, restarts=40, seed=0, inits=None):
    rng = np.random.default_rng(seed)
    bounds = [(0,1)]*(1+4*m)
    cons = [{"type": "ineq", "fun": lambda z: mean_x(z, m) - (1-c)}]
    best = (np.inf, None); starts = list(inits) if inits is not None else []
    for _ in range(restarts): starts.append(rng.random(1+4*m))
    for z0 in starts:
        try:
            r = minimize(ratio3, z0, args=(m, K, w), method="SLSQP", bounds=bounds, constraints=cons, options={"maxiter": 300, "ftol": 1e-12})
        except Exception:
            continue
        if mean_x(r.x, m) < (1-c) - 1e-9: continue
        if r.fun < best[0]: best = (r.fun, r.x)
    return best

def c_max3(K, w, m=3, restarts=25, lo=0.3815, hi=0.3845, tol=3e-6, seed=0, verbose=False):
    last = None
    while hi - lo > tol:
        mid = 0.5*(lo+hi)
        val, z = adversary_min3(K, w, mid, m=m, restarts=restarts, seed=seed, inits=[last] if last is not None else None)
        if verbose: print("   c=%.6f min ratio=%.7f" % (mid, val), flush=True)
        if val >= 1.0 - 1e-9: lo = mid
        else: hi = mid; last = z
    return lo, last

if __name__ == "__main__":
    import sys, time
    from kernel_game import make_rank_kernel, K_liu
    def f_ideal(x):
        x = np.asarray(x, float)
        return np.where(x <= 0.5, np.minimum(x, 1-x), np.sqrt(np.maximum(0.0, 0.5 - x**2)))
    kern = {"liu": K_liu, "ideal": make_rank_kernel([f_ideal])}[sys.argv[1]]
    w = tuple(float(t) for t in sys.argv[2].split(','))   # w1,w2,w3
    m = int(sys.argv[3]) if len(sys.argv) > 3 else 3
    # sanity: Cambie's Sawin-only certificate (w=(1-a*,a*,0)) should give ~0.382346
    t0 = time.time()
    c, z = c_max3(kern, w, m=m, restarts=25, verbose=False)
    print("kernel=%s w=%s m=%d : c_max=%.6f  adversary: %s  (%.0fs)" % (sys.argv[1], w, m, c, describe(z, m) if z is not None else None, time.time()-t0), flush=True)
