"""
Double-oracle / cutting-plane search over the conditionally-iid kernel class (lead task, 2026-09-08).
REVISED per lead correction (14:40): rank-1 f(x)f(y) kernels have K(eps,eps) ~ eps^2 -> 0, so the
near-degenerate adversary mu = q*delta_1 + (1-q)*delta_eps (eps->0, q=1-c) caps beta <~ 0.19.  Fix
(matches kernel_game.K_new): parametrise by the DIAGONAL VARIANCE PROFILE v(x) = Var(r_x) directly,
0 <= v(x) <= x(1-x), realised by the canonical "nested two-value" coupling

    r_x(u) = 1        for u <= t(x)
           = lam(x)    for u >  t(x)          (same shared u for every x)

with t(x), lam(x) solved in closed form from the mean (E r_x = x) and variance (Var r_x = v(x))
constraints:
    lam(x) = x - v(x)/(1-x),      t(x) = v(x) / ((1-x)^2 + v(x)).
This is realizable for ANY 0<=v(x)<=x(1-x) with no further constraint (unlike the rank-1 family).
For x,y with thresholds t(x)<=t(y) (wlog), the shared-u construction gives
    E[r_x r_y] = t(x) + (t(y)-t(x))*lam(x) + (1-t(y))*lam(x)*lam(y),
which reduces to kernel_game.K_new's three regimes when v(x) = x(1-x) on [0,1/2],
1/2-x^2 on [1/2,1/sqrt2], 0 beyond -- verified numerically below.  v(x) is free, piecewise-linear
on knots x_k=k/16 (v_0=v_16=0), 0<=v_k<=x_k(1-x_k); beta in [0.2,1.0] (lead's corrected range).

Double-oracle loop as before: outer_opt maximises the pool-relaxed min ratio (epigraph SLSQP);
kernel_game.adversary_min (which now seeds the degenerate/two-point laws via structured_inits)
supplies the true worst-case law, added to the pool if it beats the pool-relaxed candidate.
"""
import numpy as np, json, time, sys
from scipy.optimize import minimize
from kernel_game import h, K_new, adversary_min, describe, unpack, mean_x, ratio as ratio_full, c_max

LOG = open("KERNEL_OPT_run.log", "a", buffering=1)
def log(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.write(s + "\n")

NK = 17
knots = np.linspace(0, 1, NK)
minfun = np.minimum(knots, 1 - knots)
FREE = np.arange(1, NK - 1)  # v_0 = v_16 = 0 fixed

def full_v(v_free):
    v = np.zeros(NK)
    v[FREE] = v_free
    return v

def tlam(x, v_of_x):
    x = np.asarray(x, float)
    v = v_of_x(x)
    v = np.clip(v, 0.0, np.maximum(x * (1 - x), 0.0))
    denom1 = np.maximum(1 - x, 1e-12)
    lam = x - v / denom1
    denom2 = np.maximum((1 - x) ** 2 + v, 1e-18)
    t = v / denom2
    return np.clip(t, 0.0, 1.0), np.clip(lam, 0.0, 1.0)

def build_K(v_free):
    """K(x,y) from the free knot values of the variance profile v(x)."""
    v_full = full_v(v_free)
    def v_of_x(x):
        return np.interp(x, knots, v_full)
    def K(x, y):
        x = np.asarray(x, float); y = np.asarray(y, float)
        tx, lx = tlam(x, v_of_x); ty, ly = tlam(y, v_of_x)
        TX = tx[:, None]; LX = lx[:, None]; TY = ty[None, :]; LY = ly[None, :]
        t1 = np.minimum(TX, TY); t2 = np.maximum(TX, TY)
        l1 = np.where(TX <= TY, LX, LY); l2 = np.where(TX <= TY, LY, LX)
        Err = t1 + (t2 - t1) * l1 + (1 - t2) * l1 * l2
        return Err - np.outer(x, y)
    return K

def v_new_profile(x):
    """Lead's K_new baseline expressed as a variance profile, for sanity-check / warm start."""
    x = np.asarray(x, float)
    return np.where(x <= 0.5, x * (1 - x),
           np.where(x < 1/np.sqrt(2), np.maximum(0.5 - x**2, 0.0), 0.0))

def make_z(q, atoms0, atoms1, m):
    x0 = np.zeros(m); w0 = np.zeros(m)
    for i, (x, w) in enumerate(atoms0): x0[i] = x; w0[i] = w
    x1 = np.zeros(m); w1 = np.zeros(m)
    for i, (x, w) in enumerate(atoms1): x1[i] = x; w1[i] = w
    if w0.sum() == 0: w0[0] = 1.0
    if w1.sum() == 0: w1[0] = 1.0
    return np.concatenate([[q], w0, x0, w1, x1])

def two_point_law(xstar, c, m):
    if xstar < 1 - c - 1e-12:
        return None
    p = min(1.0, (1 - c) / xstar)
    return make_z(0.0, [(xstar, p), (0.0, 1 - p)], [(0.0, 1.0)], m)

def degenerate_law(eps, c, m):
    """mu = q*delta_1 + (1-q)*delta_eps, q = 1-c (the near-degenerate adversary, Liu Lemma-7 boundary)."""
    q = 1 - c
    return make_z(q, [(eps, 1.0)], [(1.0, 1.0)], m)

# ---------------- outer optimisation: maximise min-over-pool ratio ----------------
def outer_opt(pool, m, beta_bounds, restarts=12, seed=0, x0_hint=None):
    rng = np.random.default_rng(seed)
    nfree = len(FREE)  # v_free(15), beta, t
    ndim = nfree + 2

    def unpack_p(p):
        return p[:nfree], p[nfree], p[nfree + 1]

    def neg_t(p):
        return -p[-1]

    def cons_pool(p):
        v, beta, t = unpack_p(p)
        K = build_K(v)
        vals = np.array([ratio_full(z, m, K, beta) for z in pool])
        return vals - t

    cons = [{"type": "ineq", "fun": cons_pool}]
    hi_v = minfun[FREE]
    bounds = [(0.0, hi_v[i]) for i in range(nfree)] + [beta_bounds, (0.0, 2.0)]

    best = (-np.inf, None)
    starts = []
    if x0_hint is not None:
        starts.append(x0_hint)
    v_new_free = v_new_profile(knots[FREE])
    starts.append(np.concatenate([v_new_free, [0.5 * sum(beta_bounds), 0.5]]))
    for _ in range(restarts):
        v0 = rng.uniform(0, 1, nfree) * hi_v
        b0 = rng.uniform(*beta_bounds)
        starts.append(np.concatenate([v0, [b0, 0.5]]))
    for p0 in starts:
        try:
            r = minimize(neg_t, p0, method="SLSQP", bounds=bounds, constraints=cons,
                         options={"maxiter": 300, "ftol": 1e-12})
        except Exception:
            continue
        t = -r.fun
        if t > best[0]:
            best = (t, r.x)
    return best

# ---------------- double-oracle loop for a fixed target c ----------------
def certify(c, pool, m=3, beta_bounds=(0.2, 1.0), max_rounds=4, adv_restarts=60,
            outer_restarts=12, seed=0, warm=None):
    log("  certify c=%.6f  pool=%d  beta in %s" % (c, len(pool), beta_bounds))
    x0_hint = warm
    v = beta = None
    val = None
    for rnd in range(max_rounds):
        t0 = time.time()
        t_star, p_star = outer_opt(pool, m, beta_bounds, restarts=outer_restarts, seed=seed + rnd, x0_hint=x0_hint)
        if p_star is None:
            log("    round %d: outer_opt failed" % rnd); return False, (v, beta), val
        nfree = len(FREE)
        v = p_star[:nfree]; beta = p_star[nfree]
        log("    round %d: pool-relaxed t*=%.6f beta=%.5f  (%.1fs)" % (rnd, t_star, beta, time.time() - t0))
        if t_star < 1.0 - 1e-7:
            log("    pool-relaxed bound already < 1 -> infeasible at this c")
            return False, (v, beta), t_star
        K = build_K(v)
        t1 = time.time()
        val, z = adversary_min(K, beta, c, m=m, restarts=adv_restarts, seed=seed + rnd)
        log("    round %d: true worst-case ratio=%.6f  (%.1fs)  adversary: %s" %
            (rnd, val, time.time() - t1, describe(z, m) if z is not None else None))
        if val >= 1.0 - 1e-7:
            return True, (v, beta), val
        pool.append(z)
        x0_hint = p_star
    return False, (v, beta), val

def seed_pool(c0, m=3):
    pool = []
    for xstar in np.linspace(0.55, 0.75, 21):
        z = two_point_law(xstar, c0, m)
        if z is not None: pool.append(z)
    z = two_point_law(1/np.sqrt(2), c0, m)
    if z is not None: pool.append(z)
    for eps in (1e-5, 1e-4, 1e-3, 1e-2, 3e-2):
        pool.append(degenerate_law(eps, c0, m))
    from kernel_game import K_liu
    _, zliu = adversary_min(K_liu, 0.100052559862974, 0.382709087918741, m=m, restarts=40, seed=1)
    if zliu is not None: pool.append(zliu)
    return pool

def save_best(path, v, beta, c, worst_desc):
    d = {"knots": knots.tolist(), "v": full_v(v).tolist(), "beta": float(beta), "c": float(c),
         "family": "variance-profile (nested two-value coupling)",
         "worst_adversary": worst_desc, "time": time.strftime("%Y-%m-%d %H:%M:%S")}
    with open(path, "w") as fh:
        json.dump(d, fh, indent=2)

def sanity_check_K_new_match():
    """Confirm build_K with v = v_new_profile reproduces kernel_game.K_new numerically."""
    rng = np.random.default_rng(0)
    xs = rng.uniform(0, 1, 20)
    K1 = build_K(v_new_profile(knots[FREE]))
    diffs = []
    for x in xs:
        for y in xs:
            a = K1(np.array([x]), np.array([y]))[0, 0]
            b = K_new(np.array([x]), np.array([y]))[0, 0]
            diffs.append(abs(a - b))
    return max(diffs)

if __name__ == "__main__":
    m = 3
    t_start = time.time()
    log("=" * 70)
    log("Run started (variance-profile family)", time.strftime("%Y-%m-%d %H:%M:%S"))

    md = sanity_check_K_new_match()
    log("sanity: max |build_K(v_new) - K_new| over random grid =", md)

    # baseline: K_new at a few beta to know what we need to beat (cheap since K fixed, no outer_opt)
    for beta0 in (0.2, 0.3, 0.4, 0.5):
        c0, z0 = c_max(K_new, beta0, m=m, restarts=25, lo=0.3810, hi=0.383099, tol=5e-6, seed=3)
        log("K_new baseline: beta=%.2f -> c_max=%.6f" % (beta0, c0))

    c0 = 0.38284
    pool = seed_pool(c0, m)
    log("Seed pool size:", len(pool))

    lo, hi = c0, 0.383099
    best = None
    warm = None
    tol = 3e-5
    while hi - lo > tol:
        mid = 0.5 * (lo + hi)
        ok, params, val = certify(mid, pool, m=m, beta_bounds=(0.2, 1.0),
                                   max_rounds=4, adv_restarts=60, outer_restarts=10, seed=11, warm=warm)
        if ok:
            lo = mid; best = (params[0], params[1], mid)
            v, beta = params
            warm = np.concatenate([v, [beta, 1.0]])
            save_best("best_kernel.json", v, beta, mid, None)
            log("  -> c=%.6f CERTIFIED FEASIBLE" % mid)
        else:
            hi = mid
            log("  -> c=%.6f infeasible" % mid)
        log("  [lo=%.6f hi=%.6f elapsed=%.0fs]" % (lo, hi, time.time() - t_start))

    log("Done: c_max ~= %.6f" % lo)
    if best is not None:
        v, beta, cbest = best
        log("Best: beta=%.5f c=%.6f" % (beta, cbest))
        log("v =", np.round(full_v(v), 5).tolist())
        val, zfinal = adversary_min(build_K(v), beta, lo, m=m, restarts=80, seed=99)
        save_best("best_kernel.json", v, beta, lo, describe(zfinal, m) if zfinal is not None else None)

    log("Total elapsed: %.0fs" % (time.time() - t_start))
