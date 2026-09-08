"""
Task 3: scan beta for f_ideal kernel, m=4, c_max via kernel_game.c_max with tol=2e-6.
Usage: python beta_scan_ideal.py <beta> [restarts] [seed]
Appends result line to beta_scan_results.txt
"""
import sys, time
import numpy as np
from kernel_game import make_rank_kernel, c_max, describe

def f_ideal(x):
    x = np.asarray(x, float)
    return np.where(x <= 0.5, np.minimum(x, 1 - x), np.sqrt(np.maximum(0.0, 0.5 - x**2)))

K_IDEAL = make_rank_kernel([f_ideal])

if __name__ == "__main__":
    beta = float(sys.argv[1])
    restarts = int(sys.argv[2]) if len(sys.argv) > 2 else 30
    seed = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    m = 4
    t0 = time.time()
    c, z = c_max(K_IDEAL, beta, m=m, restarts=restarts, lo=0.3815, hi=0.3835, tol=2e-6, seed=seed, verbose=False)
    dt = time.time() - t0
    line = "beta=%.3f m=%d restarts=%d tol=2e-6 : c_max=%.7f  (%.0fs)" % (beta, m, restarts, c, dt)
    print(line, flush=True)
    with open("beta_scan_results.txt", "a") as f:
        f.write(line + "\n")
