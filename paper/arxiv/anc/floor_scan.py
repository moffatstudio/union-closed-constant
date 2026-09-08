"""Certification in the small-entropy regime: minimise the ratio at (w, c) = (0.810222, 0.38284) over adversaries with
E_mu h(X) >= floor, for floors 1e-4, 1e-5, 1e-6 (m = 4 atoms per component), with structured + hiding + mixed seeds.
Also: numerical check that the 'hiding' coupling for the maximal-correlation class has maximal correlation -> 0.
Lead, 2026-09-08."""
import sys, time, numpy as np
from scipy.optimize import minimize
from kernel_game import h, unpack, mean_x, ratio, describe, make_rank_kernel, structured_inits

def f_ideal(x):
    x = np.asarray(x, float)
    return np.where(x <= 0.5, np.minimum(x, 1 - x), np.sqrt(np.maximum(0.0, 0.5 - x ** 2)))
K = make_rank_kernel([f_ideal])
beta = 0.189778; c = 0.38284; m = 4

def e_h(z):
    q, w0, x0, w1, x1 = unpack(z, m)
    atoms = np.concatenate([x0, x1]); wts = np.concatenate([(1 - q) * w0, q * w1])
    return wts @ h(atoms)

def search(floor, restarts, seed):
    rng = np.random.default_rng(seed)
    bounds = [(0, 1)] * (1 + 4 * m)
    cons = [{"type": "ineq", "fun": lambda z: mean_x(z, m) - (1 - c)},
            {"type": "ineq", "fun": lambda z: e_h(z) - floor}]
    starts = structured_inits(m, rng)
    # hiding-type seeds with a third atom y and tiny weight d
    for d in (1e-2, 1e-3, 1e-4):
        for y in (0.05, 0.2, 0.5, 0.7):
            z = np.zeros(1 + 4 * m); z[0] = 1 - c; z[1:1 + m] = [1 - d, d, 0, 0]; z[1 + m:1 + 2 * m] = [0, y, 0, 0]
            z[1 + 2 * m:1 + 3 * m] = [1, 0, 0, 0]; z[1 + 3 * m:1 + 4 * m] = [1, 1, 1, 1]; starts.append(z)
    for _ in range(restarts): starts.append(rng.random(1 + 4 * m))
    best = (np.inf, None)
    for z0 in starts:
        try:
            r = minimize(ratio, z0, args=(m, K, beta), method="SLSQP", bounds=bounds, constraints=cons,
                         options={"maxiter": 400, "ftol": 1e-13})
        except Exception:
            continue
        if mean_x(r.x, m) < (1 - c) - 1e-9 or e_h(r.x) < floor - 1e-12: continue
        if r.fun < best[0]: best = (r.fun, r.x)
    return best

def maxcorr_hiding(delta, y=0.5, q=1 - 0.38284):
    """Joint law on atoms (1, 0, y): product on {1,0}, y paired only with 0. Return 2nd singular value of normalised matrix."""
    p1, p0, py = q, (1 - q) * (1 - delta), (1 - q) * delta
    # X marginal = Y marginal = (p1, p0, py). Joint: (1,1)=p1^2/(p1+p0)*... build: product on {1,0} block scaled so marginals match,
    # then y with 0. Rows X, cols Y in order (1, 0, y).
    P = np.zeros((3, 3))
    # X=1 row: must sum to p1, paired only with Y in {1,0}: proportional to (p1, p0-py) so that column sums also work.
    # Solve a doubly-constrained 3x3 with P[y,1]=P[1,y]=0, P[y,y]=0 (y paired with 0 only).
    P[2, 1] = py; P[1, 2] = py                          # (y,0) and (0,y)
    # remaining masses: row 1 total p1, row 0 total p0 - py; column 1 total p1, column 0 total p0 - py.
    A = p1 + (p0 - py)
    P[0, 0] = p1 * p1 / A; P[0, 1] = p1 * (p0 - py) / A; P[1, 0] = (p0 - py) * p1 / A; P[1, 1] = (p0 - py) ** 2 / A
    marg = P.sum(1); assert np.allclose(marg, P.sum(0)) and np.allclose(marg, [p1, p0, py])
    M = P / np.sqrt(np.outer(marg, marg))
    sv = np.linalg.svd(M, compute_uv=False)
    return sv[1]

if __name__ == "__main__":
    print("maximal correlation of the hiding coupling (should -> 0):")
    for d in (1e-1, 1e-2, 1e-3, 1e-4, 1e-6):
        print("  delta=%g  rho_m=%.6f" % (d, maxcorr_hiding(d)), flush=True)
    print("limit 2w(1-c) =", 2 * (1 - beta) * (1 - c))
    for floor in (1e-4, 1e-5, 1e-6):
        t0 = time.time()
        val, z = search(floor, restarts=150, seed=11)
        print("floor=%g : min ratio=%.8f  E_h=%.2e  %s  (%.0fs)" % (floor, val, e_h(z), describe(z, m), time.time() - t0), flush=True)
