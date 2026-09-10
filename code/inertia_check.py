"""
Inertia (count of negative eigenvalues) of the codim-2 (mean-only: perp {1,x}) projected quadratic form
Q = [-h(x_i x_j + K(x_i,x_j))] on a uniform grid, for three kernels:
  (a) K_liu   -- rank-1, f(x)=x(1-x)
  (b) f_ideal -- rank-1, f(x)=min(x,1-x) / sqrt(1/2-x^2) / 0
  (c) K_new   -- non-rank-1 comonotone/step kernel from kernel_game.py

Since the grid is uniform, quadrature weights are a constant positive scalar (dt) for every point; by
Sylvester's law of inertia a uniform positive rescaling of the bilinear form does not change the sign
pattern (count of negative/zero/positive eigenvalues), so projecting via the plain Euclidean
orthogonal-complement of {1,x} gives the same inertia as explicit dt-quadrature weighting would.

We compute the FULL eigenspectrum of the projected (n x n) matrix at each resolution (cheap: <2s for
n~1000, ~10-20s for n~2000) rather than a fixed top-k window, because K_new turns out to have a negative
count that scales with n (not a small fixed k) -- a fixed top-20 window would miss the true crossing point.

Machine rules: single process, dense matrices only (n<=1999 here => <=32MB per matrix).
"""
import numpy as np
from scipy.linalg import eigh
import time, json, sys, os

def h(x):
    x = np.clip(x, 1e-300, 1 - 1e-16)
    return -x*np.log(x) - (1-x)*np.log(1-x)

def f_liu(x):
    x = np.asarray(x, float)
    return x*(1-x)

def f_ideal(x):
    x = np.asarray(x, float)
    return np.where(x <= 0.5, np.minimum(x, 1-x), np.sqrt(np.maximum(0.0, 0.5 - x**2)))

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kernel_game import K_new as K_new_raw, K_liu as K_liu_raw

def K_liu(x, y):
    return K_liu_raw(x, y)

def K_ideal(x, y):
    fx, fy = f_ideal(x), f_ideal(y)
    return np.outer(fx, fy)

def K_new(x, y):
    return K_new_raw(x, y)

# ---------------- projected-form builder ----------------
def build_M(K, S):
    Z = np.outer(S, S) + K(S, S)
    return -h(Z)

def project(M, S, extra_vecs=None):
    n = len(S)
    cols = [np.ones(n), S]
    if extra_vecs is not None:
        cols += list(extra_vecs)
    A = np.column_stack(cols)
    AtA = A.T @ A
    Ainv = np.linalg.inv(AtA)
    P = np.eye(n) - A @ Ainv @ A.T
    H1 = P @ M @ P
    return 0.5*(H1 + H1.T)

def full_spectrum(K, dt, extra_vecs=None):
    S = np.arange(dt, 1.0, dt)
    M = build_M(K, S)
    H1 = project(M, S, extra_vecs=extra_vecs)
    vals, vecs = eigh(H1)  # full spectrum, ascending
    return vals, vecs, S

def describe_locs(vec, S, top=10):
    idx = np.argsort(-np.abs(vec))[:top]
    return sorted(float(x) for x in S[idx])

def run_kernel(name, K, dts=(0.001, 0.0005), thresh=-1e-8, describe_max=15):
    print(f"\n===== {name} =====", flush=True)
    results = {}
    for dt in dts:
        t0 = time.time()
        vals, vecs, S = full_spectrum(K, dt)
        n = len(S)
        neg_mask = vals < thresh
        kcount = int(neg_mask.sum())
        print(f"[{name}] dt={dt} n={n} rank={n-2}  negative-count(<{thresh}) = {kcount}  (elapsed {time.time()-t0:.1f}s)", flush=True)
        print(f"[{name}] dt={dt}  most negative 5: {vals[:5]}", flush=True)
        if kcount > 0:
            print(f"[{name}] dt={dt}  k-th (last negative, idx={kcount-1}) = {vals[kcount-1]:.6e}", flush=True)
        if kcount < n:
            print(f"[{name}] dt={dt}  (k+1)-th (first non-negative, idx={kcount}) = {vals[kcount]:.6e}", flush=True)
        locs = []
        n_describe = min(kcount, describe_max)
        for i in range(n_describe):
            loc = describe_locs(vecs[:, i], S)
            locs.append({"eig": float(vals[i]), "locs": loc})
        for L in locs:
            print(f"    eig={L['eig']:.6e}  concentrates near x~{L['locs']}", flush=True)
        if kcount > describe_max:
            print(f"    ... ({kcount - describe_max} more negative eigenvalues not individually described)", flush=True)
        results[dt] = dict(n=n, k=kcount, gap_lo=float(vals[kcount-1]) if kcount>0 else None,
                            gap_hi=float(vals[kcount]) if kcount<n else None,
                            most_negative5=vals[:5].tolist(), locs=locs, time=time.time()-t0)
    return results

if __name__ == "__main__":
    t0 = time.time()
    report = {}
    report['K_liu'] = run_kernel("K_liu", K_liu)
    report['f_ideal'] = run_kernel("f_ideal", K_ideal)
    report['K_new'] = run_kernel("K_new", K_new)

    # ---- verification for K_new: add the k negative eigenvectors as extra constraints, re-project ----
    print("\n===== K_new: reprojection with negative eigen-directions added as constraints =====", flush=True)
    verify = {}
    for dt in (0.001, 0.0005):
        kcount = report['K_new'][dt]['k']
        S = np.arange(dt, 1.0, dt)
        M = build_M(K_new, S)
        H1 = project(M, S)
        vals0, vecs0 = eigh(H1)
        extra = [vecs0[:, i] for i in range(kcount)]
        H2 = project(M, S, extra_vecs=extra)
        vals2 = eigh(H2, eigvals_only=True)
        neg2 = int(np.sum(vals2 < -1e-8))
        print(f"[K_new verify] dt={dt} k={kcount}  after adding {kcount} extra constraints: remaining negative count(<-1e-8) = {neg2}", flush=True)
        print(f"    smallest 5 after reprojection: {vals2[:5]}", flush=True)
        verify[dt] = dict(k=kcount, remaining_neg=neg2, smallest5_after=vals2[:5].tolist())
    report['K_new_verify'] = verify

    with open("inertia_report.json", "w") as fh:
        json.dump(report, fh, indent=2, default=str)
    print(f"\nDONE [{time.time()-t0:.1f}s]", flush=True)
