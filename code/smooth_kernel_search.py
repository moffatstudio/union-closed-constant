"""
Search for a SMOOTH rank-1 f (K(x,y)=f(x)f(y)) that:
  (a) 0 <= f(x) <= min(x,1-x)
  (b) passes Liu's codim-3 PSD check (projected onto {1,x,f}^perp), min eigenvalue at noise level
  (c) maximises c_2pt = min_{x in [0.5,0.95]} 1 - x*h(x) / [(1-beta)*h(x^2) + beta*h(x^2+f(x)^2)]
      (h in bits), beta = 0.1898.

Design idea (per lead's hint): the certificate is only sensitive to K(x,x)=f(x)^2 being close to the
"ideal" 1/2-x^2 on x in [0.62, 1/sqrt2] (where the binding two-point adversary x*=0.6909 sits). f_ideal's
PSD failure (CONCAVITY_ideal.md / INERTIA.md) is a narrow, localized mode concentrated at x~0.696-0.705,
i.e. right at the 1/sqrt2 vertical-tangent-to-zero kink. So: keep f = f_ideal exactly up to some x=xa
(<=1/sqrt2, at or near the right edge of the critical window), then replace the sharp landing at 1/sqrt2
with a much gentler Hermite taper to zero over a wider interval [xa, x3], removing the singular slope
while barely touching the critical window (xa close to 1/sqrt2) or backing off slightly into it if needed.
"""
import numpy as np
from scipy.linalg import eigh
import json, time

def h_nat(x):
    x = np.clip(x, 1e-300, 1 - 1e-16)
    return -x*np.log(x) - (1-x)*np.log(1-x)

def h_bits(x):
    x = np.clip(x, 1e-300, 1 - 1e-16)
    return -x*np.log2(x) - (1-x)*np.log2(1-x)

SQRT2 = np.sqrt(2.0)
X2 = 1.0/SQRT2  # 0.70710678...

def ideal_branch(x):
    return np.sqrt(np.maximum(0.0, 0.5 - x**2))

def cubic_hermite_01(t, p0, m0, p1, m1):
    t2 = t*t; t3 = t2*t
    h00 = 2*t3 - 3*t2 + 1
    h10 = t3 - 2*t2 + t
    h01 = -2*t3 + 3*t2
    h11 = t3 - t2
    return h00*p0 + h10*m0 + h01*p1 + h11*m1

def make_f(xa, x3, left='ideal'):
    """f = min(x,1-x) for x<=0.5; ideal sqrt branch for 0.5<x<=xa; Hermite taper xa->x3 to (0,0);
    0 beyond x3. left='ideal' keeps f_ideal's own left half unchanged (per lead: only [0.62,1/sqrt2]
    matters, so no need to touch x<=0.5)."""
    val_a = float(ideal_branch(np.array([xa]))[0])
    deriv_a = -xa/val_a if val_a > 1e-12 else -1e3
    span = x3 - xa
    def f(x):
        x = np.asarray(x, float)
        out = np.empty_like(x)
        m_left = x <= 0.5
        out[m_left] = np.minimum(x[m_left], 1-x[m_left])
        m_mid = (x > 0.5) & (x <= xa)
        out[m_mid] = ideal_branch(x[m_mid])
        m_taper = (x > xa) & (x < x3)
        t = (x[m_taper] - xa) / span
        out[m_taper] = cubic_hermite_01(t, val_a, deriv_a*span, 0.0, 0.0)
        m_zero = x >= x3
        out[m_zero] = 0.0
        return np.clip(out, 0.0, np.minimum(x, 1-x))
    return f

def realizability_ok(f, n=4001):
    x = np.linspace(1e-6, 1-1e-6, n)
    fx = f(x)
    bad = np.sum((fx < -1e-9) | (fx > np.minimum(x, 1-x) + 1e-9))
    return bad == 0, fx.min(), (fx - np.minimum(x,1-x)).max()

def c2pt(f, beta, xs=None):
    if xs is None:
        xs = np.linspace(0.5, 0.95, 4001)
    fx = f(xs)
    num = (1-beta)*h_bits(xs**2) + beta*h_bits(xs**2 + fx**2)
    val = 1 - xs*h_bits(xs)/num
    i = np.argmin(val)
    return float(val[i]), float(xs[i])

def psd_check(f, dt=0.001, k=6):
    S = np.arange(dt, 1.0, dt)
    n = len(S)
    fx = f(S)
    Z = np.outer(S, S) + np.outer(fx, fx)
    M = -h_nat(Z)
    A = np.column_stack([np.ones(n), S, fx])
    AtA = A.T @ A
    P = np.eye(n) - A @ np.linalg.inv(AtA) @ A.T
    H1 = P @ M @ P
    H1 = 0.5*(H1+H1.T)
    vals = eigh(H1, eigvals_only=True, subset_by_index=[0, k-1])
    return vals

if __name__ == "__main__":
    beta = 0.1898
    t0 = time.time()

    # baselines
    def f_liu(x):
        x = np.asarray(x, float); return x*(1-x)
    def f_ideal(x):
        x = np.asarray(x, float)
        return np.where(x <= 0.5, np.minimum(x, 1-x), np.sqrt(np.maximum(0.0, 0.5 - x**2)))

    c_liu, x_liu = c2pt(f_liu, beta)
    c_ideal, x_ideal = c2pt(f_ideal, beta)
    print(f"baseline f_liu:   c_2pt={c_liu:.6f} at x={x_liu:.4f}", flush=True)
    print(f"baseline f_ideal: c_2pt={c_ideal:.6f} at x={x_ideal:.4f}", flush=True)
    vals_liu = psd_check(f_liu, dt=0.001)
    vals_ideal = psd_check(f_ideal, dt=0.001)
    print(f"  f_liu   codim-3 min eig (dt=0.001): {vals_liu}", flush=True)
    print(f"  f_ideal codim-3 min eig (dt=0.001): {vals_ideal}", flush=True)

    print("\n=== grid search over (xa, x3) ===", flush=True)
    results = []
    xa_grid = [0.60, 0.62, 0.64, 0.66, 0.68, 0.695, 0.703, X2]
    x3_grid = [0.72, 0.75, 0.78, 0.82, 0.86, 0.90, 0.95]
    for xa in xa_grid:
        for x3 in x3_grid:
            if x3 <= xa + 0.01:
                continue
            f = make_f(xa, x3)
            ok, fmin, over = realizability_ok(f)
            if not ok:
                continue
            vals = psd_check(f, dt=0.001, k=4)
            minval = float(vals[0])
            c, xc = c2pt(f, beta)
            results.append(dict(xa=xa, x3=x3, minval=minval, c2pt=c, xc=xc))
            print(f"xa={xa:.3f} x3={x3:.3f}  PSD min={minval:.3e}  c2pt={c:.6f} (argmin x={xc:.3f})", flush=True)

    with open("smooth_kernel_search_coarse.json", "w") as fh:
        json.dump(results, fh, indent=2)
    print(f"\n[{time.time()-t0:.1f}s] coarse search done", flush=True)
