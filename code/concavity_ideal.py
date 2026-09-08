"""
PSD / concavity check for the new kernel K(x,y) = f_ideal(x) f_ideal(y), following Liu (2306.08824)
Section IV (Lemma 11 / Theorem 12) and Section V-A's numerical PSD hypothesis (frankl3.m).

Convention: x = s-bar (zero-probability of the "bar" bit), matching kernel_game.py / Section V of the paper.
h(x) = -x ln x - (1-x) ln(1-x)  [natural log, as in kernel_game.py].
Z(x,y) = xy + f(x) f(y).  We test PSD of the quadratic form nu -> -int int h(Z) dnu dnu
on {int dnu = 0, int x dnu = 0} (weak/"stronger" condition, codim 2) and on
{int dnu = 0, int x dnu = 0, int f(x) dnu = 0} (the actual Theorem-12 condition, codim 3).

Machine rules: single process, dense 2500x2500 float64 matrices only (~50MB each, well under 2GB).
"""
import numpy as np
from scipy.linalg import eigh
from scipy.optimize import linprog
import time, json

# ---------------- kernels / entropy ----------------
def h(x):
    x = np.clip(x, 1e-300, 1 - 1e-16)
    return -x*np.log(x) - (1-x)*np.log(1-x)

def f_liu(x):
    x = np.asarray(x, float)
    return x*(1-x)

def f_ideal(x):
    x = np.asarray(x, float)
    return np.where(x <= 0.5, np.minimum(x, 1-x), np.sqrt(np.maximum(0.0, 0.5 - x**2)))

def make_smoothed_minmax(lam):
    def f(x):
        x = np.asarray(x, float)
        return np.minimum(f_ideal(x), lam*np.minimum(x, 1-x))
    return f

def quintic_hermite(t, p0, m0, p1, m1):
    # t in [0,1]; quintic (degree 5) with zero 2nd derivative at ends too -> C1 (and C2) blend
    t2 = t*t; t3 = t2*t
    h00 = 1 - 10*t3 + 15*t2*t2 - 6*t2*t2*t
    h10 = t - 6*t3 + 8*t2*t2 - 3*t2*t2*t
    h01 = 10*t3 - 15*t2*t2 + 6*t2*t2*t
    h11 = -4*t3 + 7*t2*t2 - 3*t2*t2*t
    return h00*p0 + h10*m0 + h01*p1 + h11*m1

def make_f_ideal_c1(w1=0.03, w2=0.03):
    """C1 smoothing of f_ideal: quintic-Hermite blend across [0.5-w1,0.5+w1] and
    across [1/sqrt2-w2, 1/sqrt2] (forcing derivative 0 at 1/sqrt2, matching the flat
    zero-continuation for x>1/sqrt2)."""
    xm = 0.5
    xr = 1.0/np.sqrt(2.0)
    # values/derivatives of the two raw branches at window edges
    def branch_lo(x): return np.minimum(x, 1-x)                       # x<=0.5 branch, deriv +1 near 0.5-
    def branch_hi(x): return np.sqrt(np.maximum(0.0, 0.5 - x**2))     # 0.5<x<=1/sqrt2 branch
    def branch_hi_deriv(x): return -x/np.sqrt(np.maximum(1e-12, 0.5-x**2))

    a0, a1 = xm - w1, xm + w1
    p0a, m0a = branch_lo(a0), 1.0
    p1a, m1a = branch_hi(a1), branch_hi_deriv(a1)

    b0, b1 = xr - w2, xr
    p0b, m0b = branch_hi(b0), branch_hi_deriv(b0)
    p1b, m1b = 0.0, 0.0

    def f(x):
        x = np.asarray(x, float)
        out = np.empty_like(x)
        m1_ = x <= a0
        out[m1_] = branch_lo(x[m1_])
        m2_ = (x > a0) & (x < a1)
        t = (x[m2_]-a0)/(a1-a0)
        out[m2_] = quintic_hermite(t, p0a, m0a*(a1-a0), p1a, m1a*(a1-a0))
        m3_ = (x >= a1) & (x <= b0)
        out[m3_] = branch_hi(x[m3_])
        m4_ = (x > b0) & (x < b1)
        t = (x[m4_]-b0)/(b1-b0)
        out[m4_] = quintic_hermite(t, p0b, m0b*(b1-b0), p1b, m1b*(b1-b0))
        m5_ = x >= b1
        out[m5_] = 0.0
        return out
    return f

# ---------------- grid PSD check ----------------
def grid_check(f, dt=0.0004, mode='full', k=10, want_vecs=False):
    """mode='full': project out {1,x,f(x)} (Theorem-12 condition, codim 3).
       mode='mean_only': project out {1,x} only (stronger condition, codim 2)."""
    S = np.arange(dt, 1.0, dt)
    n = len(S)
    fx = f(S)
    Z = np.outer(S, S) + np.outer(fx, fx)
    M = -h(Z)
    if mode == 'full':
        A = np.column_stack([np.ones(n), S, fx])
    else:
        A = np.column_stack([np.ones(n), S])
    AtA = A.T @ A
    Ainv = np.linalg.inv(AtA)
    P = np.eye(n) - A @ Ainv @ A.T
    H1 = P @ M @ P
    H1 = 0.5*(H1 + H1.T)
    if want_vecs:
        vals, vecs = eigh(H1, subset_by_index=[0, k-1])
        return vals, vecs, S, n
    else:
        vals = eigh(H1, eigvals_only=True, subset_by_index=[0, k-1])
        return vals, S, n

# ---------------- random-measure concavity sampling ----------------
def J(atoms, wts, f):
    fx = f(atoms)
    Z = np.outer(atoms, atoms) + np.outer(fx, fx)
    return wts @ h(Z) @ wts

def gen_measure(rng, k):
    x = rng.random(k)
    w = rng.dirichlet(np.ones(k))
    return x, w

def match_moments(rng, target_mean, target_d, f, k, tries=60):
    """Find atoms/weights (k atoms) on the simplex matching E[X]=target_mean, E[f(X)]=target_d."""
    for _ in range(tries):
        x = rng.random(k)
        fx = f(x)
        A_eq = np.vstack([np.ones(k), x, fx])
        b_eq = np.array([1.0, target_mean, target_d])
        c = rng.standard_normal(k)  # random objective -> varied feasible vertex/solution
        res = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=[(0, 1)]*k, method='highs')
        if res.success:
            w = np.clip(res.x, 0, None)
            if w.sum() > 1e-9:
                w = w / w.sum()
                return x, w
    return None, None

def random_concavity_test(f, n_trials=400, seed=0):
    rng = np.random.default_rng(seed)
    worst = (np.inf, None)
    n_valid = 0
    n_violations = 0
    for _ in range(n_trials):
        k1 = rng.integers(3, 6)
        x1, w1 = gen_measure(rng, k1)
        c = float(w1 @ x1)
        d = float(w1 @ f(x1))
        k2 = int(rng.integers(3, 6))
        x2, w2 = match_moments(rng, c, d, f, k2)
        if x2 is None:
            continue
        n_valid += 1
        Jm = 0.5*J(x1, w1, f) + 0.5*J(x2, w2, f)
        # mixture measure (mu1+mu2)/2
        xa = np.concatenate([x1, x2])
        wa = np.concatenate([0.5*w1, 0.5*w2])
        Javg = J(xa, wa, f)
        gap = Javg - Jm  # concavity requires Javg >= Jm  (J is -integral h, so want gap>=0 for -h concave... check sign)
        if gap < worst[0]:
            worst = (gap, (x1, w1, x2, w2, c, d))
        if gap < -1e-10:
            n_violations += 1
    return worst, n_valid, n_violations, n_trials


if __name__ == "__main__":
    t0 = time.time()
    report = {}

    print("=== Task 1: reproduce Liu grid check (f_liu, codim-3) ===", flush=True)
    vals, S, n = grid_check(f_liu, dt=0.0004, mode='full', k=10)
    print(f"n={n} grid points; smallest 10 eigenvalues:\n{vals}", flush=True)
    report['liu_full'] = vals.tolist()

    print("=== Task 1b: f_liu, codim-2 (mean-only) ===", flush=True)
    vals2, S, n = grid_check(f_liu, dt=0.0004, mode='mean_only', k=10)
    print(f"smallest 10 eigenvalues:\n{vals2}", flush=True)
    report['liu_mean_only'] = vals2.tolist()

    print(f"[{time.time()-t0:.1f}s elapsed]", flush=True)

    print("=== Task 2: f_ideal, codim-3 (Theorem-12 condition) ===", flush=True)
    vals3, vecs3, S, n = grid_check(f_ideal, dt=0.0004, mode='full', k=10, want_vecs=True)
    print(f"smallest 10 eigenvalues:\n{vals3}", flush=True)
    report['ideal_full'] = vals3.tolist()

    print("=== Task 2b: f_ideal, codim-2 (stronger, mean-only) ===", flush=True)
    vals4, vecs4, S, n = grid_check(f_ideal, dt=0.0004, mode='mean_only', k=10, want_vecs=True)
    print(f"smallest 10 eigenvalues:\n{vals4}", flush=True)
    report['ideal_mean_only'] = vals4.tolist()

    print(f"[{time.time()-t0:.1f}s elapsed]", flush=True)

    # locate negative eigenvector concentration
    for label, vals_, vecs_ in [("ideal_full", vals3, vecs3), ("ideal_mean_only", vals4, vecs4)]:
        v0 = vals_[0]
        if v0 < -1e-8:
            vec0 = vecs_[:, 0]
            idx_sorted = np.argsort(-np.abs(vec0))[:15]
            locs = sorted(S[idx_sorted])
            print(f"[{label}] negative min-eigval={v0:.6e}; top-|component| x-locations: {np.round(locs,4)}", flush=True)
            report[label+'_neg_locs'] = [float(x) for x in locs]

    print("=== Task 3: smoothed variants ===", flush=True)
    for lam in [0.9, 0.8]:
        f_s = make_smoothed_minmax(lam)
        vf, S, n = grid_check(f_s, dt=0.0004, mode='full', k=6)
        vm, S, n = grid_check(f_s, dt=0.0004, mode='mean_only', k=6)
        print(f"lam={lam}: full-cond smallest6={vf}  mean-only smallest6={vm}", flush=True)
        report[f'smoothed_lam{lam}_full'] = vf.tolist()
        report[f'smoothed_lam{lam}_mean_only'] = vm.tolist()

    f_c1 = make_f_ideal_c1(w1=0.03, w2=0.03)
    vf, S, n = grid_check(f_c1, dt=0.0004, mode='full', k=6)
    vm, S, n = grid_check(f_c1, dt=0.0004, mode='mean_only', k=6)
    print(f"C1-smoothed f_ideal: full-cond smallest6={vf}  mean-only smallest6={vm}", flush=True)
    report['c1_smoothed_full'] = vf.tolist()
    report['c1_smoothed_mean_only'] = vm.tolist()

    print(f"[{time.time()-t0:.1f}s elapsed]", flush=True)

    print("=== Task 4: random-measure concavity sampling ===", flush=True)
    for label, f_ in [("f_liu", f_liu), ("f_ideal", f_ideal),
                       ("f_ideal_lam0.9", make_smoothed_minmax(0.9)),
                       ("f_ideal_lam0.8", make_smoothed_minmax(0.8)),
                       ("f_ideal_c1", f_c1)]:
        worst, n_valid, n_viol, n_trials = random_concavity_test(f_, n_trials=300, seed=42)
        print(f"[{label}] n_valid_pairs={n_valid}/{n_trials} n_violations={n_viol} worst_gap={worst[0]:.6e}", flush=True)
        report[f'random_{label}'] = {'n_valid': n_valid, 'n_trials': n_trials, 'n_violations': n_viol, 'worst_gap': float(worst[0])}
        if worst[0] < -1e-9 and worst[1] is not None:
            x1, w1, x2, w2, c, d = worst[1]
            print(f"    worst case: c(mean)={c:.4f} d(Ef)={d:.4f}\n    mu1 atoms={np.round(x1,4)} w={np.round(w1,4)}\n    mu2 atoms={np.round(x2,4)} w={np.round(w2,4)}", flush=True)

    with open("concavity_ideal_report.json", "w") as fh:
        json.dump(report, fh, indent=2)
    print(f"DONE [{time.time()-t0:.1f}s elapsed]", flush=True)
