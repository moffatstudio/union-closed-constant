"""
PCHIP-spline parametrization of f, jointly optimizing c_2pt subject to a PSD penalty.
Knots (x fixed, y free except at 0, 1, 0.62, 0.6909 which are pinned):
  x=0.00 -> y=0                     (realizability endpoint)
  x=0.25 -> y=p[0]   free, [0, 0.25]
  x=0.50 -> y=p[1]   free, [0, 0.50]
  x=0.62 -> y=ideal(0.62)=0.34      PINNED (critical window left edge)
  x=0.6909 -> y=ideal(0.6909)=0.1505 PINNED (adversary point x*)
  x=0.7071 -> y=p[2]  free, [0, 0.2929]   (relax the singular right edge)
  x=0.78 -> y=p[3]   free, [0, 0.22]
  x=0.90 -> y=p[4]   free, [0, 0.10]
  x=1.00 -> y=0                     (realizability endpoint)
PCHIP (monotone-safe shape-preserving cubic Hermite) through these 9 knots, then clipped to
[0, min(x,1-x)] for hard realizability.
"""
import numpy as np
from scipy.interpolate import PchipInterpolator
from scipy.optimize import differential_evolution
from scipy.linalg import eigh
import json, time

def h_nat(x):
    x = np.clip(x, 1e-300, 1 - 1e-16)
    return -x*np.log(x) - (1-x)*np.log(1-x)
def h_bits(x):
    x = np.clip(x, 1e-300, 1 - 1e-16)
    return -x*np.log2(x) - (1-x)*np.log2(1-x)

X1, XSTAR, X2 = 0.62, 0.6909, 1.0/np.sqrt(2.0)
Y1 = float(np.sqrt(0.5 - X1**2))       # 0.34
YSTAR = float(np.sqrt(0.5 - XSTAR**2)) # 0.1505...

XK_FIXED = [0.0, X1, XSTAR]
XK_FREE  = [0.25, 0.50, X2, 0.78, 0.90]
BOUNDS   = [(0,0.25), (0,0.50), (0,0.5-X2**2 if 0.5-X2**2>0 else 0.05), (0,0.22), (0,0.10)]
# fix small negative rounding for X2 bound: 0.5-X2^2 ~ 0, so allow a small window
BOUNDS[2] = (0.0, 0.05)

def build_f(p):
    y25, y50, y707, y78, y90 = p
    xk = np.array([0.0, 0.25, 0.5, X1, XSTAR, X2, 0.78, 0.90, 1.0])
    yk = np.array([0.0, y25,  y50, Y1, YSTAR, y707, y78, y90, 0.0])
    pchip = PchipInterpolator(xk, yk)
    def f(x):
        x = np.asarray(x, float)
        out = pchip(x)
        out = np.clip(out, 0.0, np.minimum(x, 1-x))
        return out
    return f

def c2pt(f, beta, xs=None):
    if xs is None:
        xs = np.linspace(0.5, 0.95, 3001)
    fx = f(xs)
    num = (1-beta)*h_bits(xs**2) + beta*h_bits(xs**2 + fx**2)
    val = 1 - xs*h_bits(xs)/num
    i = np.argmin(val)
    return float(val[i]), float(xs[i])

def psd_min(f, dt=0.001):
    S = np.arange(dt, 1.0, dt)
    n = len(S)
    fx = f(S)
    Z = np.outer(S, S) + np.outer(fx, fx)
    M = -h_nat(Z)
    A = np.column_stack([np.ones(n), S, fx])
    P = np.eye(n) - A @ np.linalg.inv(A.T @ A) @ A.T
    H1 = P @ M @ P
    H1 = 0.5*(H1+H1.T)
    return float(eigh(H1, eigvals_only=True, subset_by_index=[0,0])[0])

BETA = 0.1898
_evals = {"n": 0}

def objective(p, dt=0.003):
    _evals["n"] += 1
    f = build_f(p)
    c, xc = c2pt(f, BETA)
    m = psd_min(f, dt=dt)  # coarse for speed inside DE loop
    penalty = max(0.0, -m) * 500.0   # heavy penalty for PSD violation
    return -(c) + penalty

if __name__ == "__main__":
    from scipy.optimize import minimize
    t0 = time.time()
    print("Running differential_evolution search (coarse dt=0.003)...", flush=True)
    res = differential_evolution(objective, BOUNDS, maxiter=40, popsize=10, tol=1e-9,
                                  seed=0, polish=False, workers=1, disp=True)
    p0 = res.x
    print(f"DE done in {time.time()-t0:.1f}s, n_evals={_evals['n']}", flush=True)

    print("Local polish at dt=0.0015...", flush=True)
    res2 = minimize(lambda p: objective(p, dt=0.0015), p0, method="Nelder-Mead",
                     bounds=BOUNDS, options={"maxiter": 300, "xatol": 1e-5, "fatol": 1e-8})
    p_best = res2.x
    f_best = build_f(p_best)
    c_best, xc_best = c2pt(f_best, BETA)
    m_coarse = psd_min(f_best, dt=0.001)
    m_fine = psd_min(f_best, dt=0.0004)
    print(f"\nBest params: y25={p_best[0]:.5f} y50={p_best[1]:.5f} y707={p_best[2]:.5f} y78={p_best[3]:.5f} y90={p_best[4]:.5f}", flush=True)
    print(f"c_2pt={c_best:.6f} at x={xc_best:.4f}", flush=True)
    print(f"PSD min eig: dt=0.001 -> {m_coarse:.3e}   dt=0.0004 -> {m_fine:.3e}", flush=True)
    print(f"n_evals={_evals['n']}  time={time.time()-t0:.1f}s", flush=True)

    out = dict(params=dict(y25=p_best[0], y50=p_best[1], y707=p_best[2], y78=p_best[3], y90=p_best[4]),
               c2pt=c_best, xc=xc_best, psd_coarse=m_coarse, psd_fine=m_fine)
    with open("smooth_kernel_opt_best.json", "w") as fh:
        json.dump(out, fh, indent=2)
