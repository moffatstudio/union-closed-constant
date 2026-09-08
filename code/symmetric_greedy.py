import math, sys
from functools import lru_cache
from symmetric_dp import slice_family_tables, h, max_freq
def greedy(n, K):
    N = slice_family_tables(n, K)
    def u(i, w): return N[i+1][w]/N[i][w]
    @lru_cache(maxsize=None)
    def V(i, wa, wb):
        if i == n or N[i][wa] == 0 or N[i][wb] == 0: return 0.0
        ua, vb = u(i,wa), u(i,wb); lo, hi = max(0.0, ua+vb-1.0), min(ua, vb); s = min(max(0.5, lo), hi)
        tot = h(s) - 0.5*(h(ua)+h(vb))
        for (x,y,w) in ((0,0,s),(0,1,ua-s),(1,0,vb-s),(1,1,1-ua-vb+s)):
            if w > 1e-13 and N[i+1][wa+x] > 0 and N[i+1][wb+y] > 0: tot += w*V(i+1, wa+x, wb+y)
        return tot
    return V(0,0,0)
n = int(sys.argv[1])
print("greedy on single slices n=%d" % n)
for k in range(1, n//2+1): print("  k=%2d p=%.4f greedy=%+.4f" % (k, k/n, greedy(n,[k])))
worst = (1.0, None)
for k in range(0, n+1):
    for l in range(k+1, n+1):
        K=[k,l]; p = max_freq(n,K)
        if p >= 0.5: continue
        g = greedy(n,K)
        if g <= 1e-9 and p < worst[0]: worst = (p,K); print("  greedy two-slice barrier K=%s p=%.4f g=%+.3e" % (K,p,g), flush=True)
print("worst two-slice greedy barrier n=%d:" % n, worst)
# three slices, coarse
worst3 = (1.0, None)
for k in range(0, n+1):
    for l in range(k+1, n+1):
        for m in range(l+1, n+1):
            K=[k,l,m]; p = max_freq(n,K)
            if p >= 0.5: continue
            g = greedy(n,K)
            if g <= 1e-9 and p < worst3[0]: worst3 = (p,K); print("  greedy three-slice barrier K=%s p=%.4f g=%+.3e" % (K,p,g), flush=True)
print("worst three-slice greedy barrier n=%d:" % n, worst3)
