import sys, time, random
from seqcoupling_dp import greedy_gain, max_gain, max_freq, is_union_closed
mode = sys.argv[1]; n = int(sys.argv[2])
N = 1 << n
if mode == "exhaustive":
    best = (1.0, None)
    for mask in range(1, 1 << N):
        F = [S for S in range(N) if (mask >> S) & 1]
        if len(F) < 2: continue
        p = max_freq(F, n)
        if p >= best[0]: continue
        g = greedy_gain(F, n)
        if g <= 1e-9:
            best = (p, F); print("greedy barrier n=%d p=%.5f F=%s uc=%s g=%.3e" % (n, p, F, is_union_closed(F), g), flush=True)
    print("FINAL greedy barrier n=%d: p=%.5f F=%s" % (n, best[0], best[1]))
else:
    PMAX = float(sys.argv[3]); seconds = float(sys.argv[4]); random.seed(n)
    def score(F):
        if len(F) < 2: return 9.0
        p = max_freq(F, n)
        if p > PMAX: return 9.0 + (p-PMAX)
        return greedy_gain(F, n)
    best_global = (9.0, None); t0 = time.time(); restarts = 0
    while time.time()-t0 < seconds:
        restarts += 1
        F = sorted(random.sample(range(N), random.randint(2, max(3, N//3)))); cur = score(F); stall = 0
        while stall < 4*N and time.time()-t0 < seconds:
            S = random.randrange(N); G = sorted(set(F) ^ {S}); sc = score(G)
            if sc <= cur + 1e-12:
                stall = 0 if sc < cur - 1e-12 else stall+1; F, cur = G, sc
            else: stall += 1
        if cur < best_global[0]:
            best_global = (cur, F)
            print("greedy n=%d pmax=%.3f restart %d: g=%.5f p=%.4f uc=%s F=%s" % (n, PMAX, restarts, cur, max_freq(F,n), is_union_closed(F), F), flush=True)
    print("DONE greedy n=%d pmax=%.3f restarts=%d best g=%.6f F=%s" % (n, PMAX, restarts, best_global[0], best_global[1]))
