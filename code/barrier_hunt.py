# Exhaustive: for every family F on [n] (n=3,4), compute max-freq and G_max (best sequential coupling gain).
# Report the smallest max-frequency among families with G_max <= 1e-9 (barrier for class S at this n),
# and the same for the iid method (should approach psi from above for larger n).
import itertools, math, sys, time
from seqcoupling_dp import max_gain, iid_gain, max_freq, is_union_closed
n = int(sys.argv[1])
N = 1 << n
t0=time.time()
best_S = (1.0, None); best_iid = (1.0, None)
rows=[]
for mask in range(1, 1 << N):
    F = [S for S in range(N) if (mask >> S) & 1]
    if len(F) < 2: continue
    p = max_freq(F, n)
    if p >= min(best_S[0], best_iid[0]) : continue
    gi = iid_gain(F, n)
    if gi <= 1e-9 and p < best_iid[0]:
        best_iid = (p, F)
    if p < best_S[0]:
        gs = max_gain(F, n)
        if gs <= 1e-9:
            best_S = (p, F)
            print("new S-barrier: p=%.5f F=%s uc=%s Gmax=%.3e" % (p, F, is_union_closed(F), gs), flush=True)
print("n=%d  iid barrier p=%.5f F=%s" % (n, best_iid[0], best_iid[1]))
print("n=%d  S   barrier p=%.5f F=%s" % (n, best_S[0], best_S[1]))
print("time", time.time()-t0)
