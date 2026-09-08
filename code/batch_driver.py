"""
Driver for task 1 (robustness sweep): runs a fixed list of (beta,c,m) combos sequentially
within one process (avoids repeated python startup / import overhead), respecting the
"at most 2 concurrent processes" machine rule -- launch this script twice, once with
half="A" and once with half="B", each covering disjoint combos.
"""
import sys, time
from robustness_ideal import run, describe, mean_x

BETAS = [0.15, 0.20]
CS = [0.38280, 0.38284, 0.38290]
MS = [4, 5, 6]
RESTARTS = 300
SEED = 1

ALL_COMBOS = [(beta, c, m) for m in MS for beta in BETAS for c in CS]  # 18 combos

def main(half):
    combos = ALL_COMBOS[0::2] if half == "A" else ALL_COMBOS[1::2]
    print("driver %s: %d combos" % (half, len(combos)), flush=True)
    for beta, c, m in combos:
        t0 = time.time()
        val, z, dt, ninit = run(beta, c, m, RESTARTS, SEED)
        mx = mean_x(z, m) if z is not None else -1
        print("RESULT beta=%.2f c=%.5f m=%d restarts=%d(+%d struct) : min_ratio=%.8f mean_x=%.6f time=%.0fs" %
              (beta, c, m, RESTARTS, ninit, val, mx, dt), flush=True)
        print("  adversary: %s" % (describe(z, m) if z is not None else None), flush=True)
    print("driver %s: DONE" % half, flush=True)

if __name__ == "__main__":
    main(sys.argv[1])
