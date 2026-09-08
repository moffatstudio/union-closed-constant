# Local search for sequential-coupling barrier families: minimise G_max(F) over families F on [n]
# with max frequency <= PMAX. Moves: toggle one set in/out. Restarts from random families.
import random, sys, time, math
from seqcoupling_dp import max_gain, max_freq, is_union_closed
n = int(sys.argv[1]); PMAX = float(sys.argv[2]); seconds = float(sys.argv[3]); seed = int(sys.argv[4]) if len(sys.argv)>4 else 0
random.seed(seed); N = 1 << n
def score(F):
    if len(F) < 2: return 9.0
    p = max_freq(F, n)
    if p > PMAX: return 9.0 + (p - PMAX)
    return max_gain(F, n)
best_global = (9.0, None); t0 = time.time(); restarts = 0
while time.time() - t0 < seconds:
    restarts += 1
    F = sorted(random.sample(range(N), random.randint(2, max(3, N//3))))
    cur = score(F); stall = 0
    while stall < 3*N and time.time() - t0 < seconds:
        S = random.randrange(N)
        G = sorted(set(F) ^ {S})
        sc = score(G)
        if sc <= cur + 1e-12:
            if sc < cur - 1e-12: stall = 0
            else: stall += 1
            F, cur = G, sc
        else:
            stall += 1
    if cur < best_global[0]:
        best_global = (cur, F)
        print("n=%d pmax=%.3f restart %d: Gmax=%.5f p=%.4f uc=%s F=%s" % (n, PMAX, restarts, cur, max_freq(F,n), is_union_closed(F), F), flush=True)
print("DONE n=%d pmax=%.3f restarts=%d best Gmax=%.6f F=%s" % (n, PMAX, restarts, best_global[0], best_global[1]))
