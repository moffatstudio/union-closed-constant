"""
Explicitly evaluate the degenerate adversary law mu = q*delta_{x=1} + (1-q)*delta_{x=eps} (eps->0)
flagged by the lead: for any rank-1 kernel with f(eps)~eps (f_ideal included), K(eps,*) -> 0, so this
law's ratio -> 2*(1-beta)*(1-c) as eps->0 with q=1-c (mean_x exactly at the floor).
Reports: (a) the analytic limit 2*(1-beta)*(1-c), (b) the numerically evaluated ratio at eps in
{1e-2,1e-3,1e-4,1e-6} with q=1-c exactly, (c) a fine 1-D scan over q around 1-c (eps=1e-6 fixed)
to check q=1-c is really the worst case (not just a convenient guess).
"""
import numpy as np
from kernel_game import make_rank_kernel, ratio, mean_x

def f_ideal(x):
    x = np.asarray(x, float)
    return np.where(x <= 0.5, np.minimum(x, 1 - x), np.sqrt(np.maximum(0.0, 0.5 - x**2)))

K_IDEAL = make_rank_kernel([f_ideal])

def z_degenerate(q, eps, m):
    z = np.zeros(1 + 4*m)
    z[0] = q
    z[1:1+m] = 1.0/m          # w0
    z[1+m:1+2*m] = eps        # x0 atoms
    z[1+2*m:1+3*m] = 1.0/m    # w1
    z[1+3*m:1+4*m] = 1.0      # x1 atoms
    return z

def report(beta, c, m=3):
    q_floor = 1 - c
    print(f"--- beta={beta:.3f}  c={c:.5f}  (1-c={1-c:.6f}) ---")
    print(f"  analytic limit 2*(1-beta)*(1-c) = {2*(1-beta)*(1-c):.6f}   "
          f"({'CERTIFICATE FAILS (<1)' if 2*(1-beta)*(1-c) < 1 else 'ok (>=1)'})")
    for eps in (1e-2, 1e-3, 1e-4, 1e-6):
        z = z_degenerate(q_floor, eps, m)
        r = ratio(z, m, K_IDEAL, beta)
        mx = mean_x(z, m)
        print(f"  eps={eps:.0e}  q=1-c={q_floor:.6f} : ratio={r:.7f}  mean_x={mx:.7f}")
    # fine scan over q (eps fixed at 1e-6) to find the true worst q near the floor
    eps = 1e-6
    qs = np.linspace(max(0.0, q_floor - 0.05), min(1.0, q_floor + 0.10), 61)
    vals = []
    for q in qs:
        z = z_degenerate(q, eps, m)
        if mean_x(z, m) < q_floor - 1e-9:
            continue
        vals.append((ratio(z, m, K_IDEAL, beta), q))
    vals.sort()
    best_r, best_q = vals[0]
    print(f"  best over q-scan (eps=1e-6, feasible q>=1-c): min ratio={best_r:.7f} at q={best_q:.6f}")
    print()

if __name__ == "__main__":
    for beta in (0.10, 0.15, 0.19, 0.20, 0.25, 0.30):
        for c in (0.38280, 0.38284, 0.38290):
            report(beta, c)
