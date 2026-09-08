"""
Sequential-coupling entropy game for SYMMETRIC families F = union of full slices {S : |S| in K}, K subset of {0..n}.
Under uniform measure on F, the conditional P(next bit = 0 | prefix) depends only on (i, w) with w = weight of prefix.
So the DP state is (i, wa, wb): O(n^3) states, each a 1-D concave maximisation. Lets us probe the asymptotic
barrier of the sequential-coupling class on Chase-Lovett-type families for n up to ~100.

G_max(F) = max over sequential couplings of  sum_i E[h(s_i) - (h(u_i)+h(v_i))/2]   (>0 means the method beats F).
Also reports the iid value.
"""
import math, sys
from functools import lru_cache
from math import comb

def h(x):
    if x <= 0.0 or x >= 1.0: return 0.0
    return -(x*math.log2(x) + (1-x)*math.log2(1-x))

def slice_family_tables(n, K):
    K = sorted(set(K))
    # N[i][w] = number of sets in F whose first i coordinates have weight w  = sum_{k in K} C(n-i, k-w)
    N = [[0]*(n+1) for _ in range(n+1)]
    for i in range(n+1):
        for w in range(i+1):
            N[i][w] = sum(comb(n-i, k-w) for k in K if 0 <= k-w <= n-i)
    return N

def gains(n, K, mode="seq"):
    N = slice_family_tables(n, K)
    def u(i, w):
        return N[i+1][w] / N[i][w]   # P(bit i+1 = 0 | prefix weight w)
    sys.setrecursionlimit(100000)

    @lru_cache(maxsize=None)
    def V(i, wa, wb):
        if i == n: return 0.0
        if N[i][wa] == 0 or N[i][wb] == 0: return 0.0
        ua, vb = u(i, wa), u(i, wb)
        base = -0.5*(h(ua)+h(vb))
        def fut(s):
            tot = h(s)
            for (x, y, w) in ((0,0,s),(0,1,ua-s),(1,0,vb-s),(1,1,1-ua-vb+s)):
                if w > 1e-13:
                    na, nb = wa+x, wb+y
                    if N[i+1][na] > 0 and N[i+1][nb] > 0:
                        tot += w*V(i+1, na, nb)
            return tot
        if mode == "iid":
            return base + fut(ua*vb)
        lo, hi = max(0.0, ua+vb-1.0), min(ua, vb)
        if hi - lo < 1e-13: return base + fut(lo)
        gr = (math.sqrt(5)-1)/2
        x1 = hi - gr*(hi-lo); x2 = lo + gr*(hi-lo); f1, f2 = fut(x1), fut(x2)
        for _ in range(50):
            if f1 < f2: lo = x1; x1 = x2; f1 = f2; x2 = lo + gr*(hi-lo); f2 = fut(x2)
            else: hi = x2; x2 = x1; f2 = f1; x1 = hi - gr*(hi-lo); f1 = fut(x1)
        return base + max(f1, f2, fut(lo), fut(hi))
    return V(0, 0, 0)

def max_freq(n, K):
    m = sum(comb(n, k) for k in K)
    return sum(comb(n, k)*k for k in K) / (n*m)

if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 30
    print("single slices, n=%d" % n)
    for k in range(1, n//2 + 1):
        K = [k]
        print("  K=%-6s p=%.4f  iid=%+.4f  seq=%+.4f" % (K, max_freq(n,K), gains(n,K,"iid"), gains(n,K,"seq")))
    print("two slices {k, l}, n=%d (only those with seq <= 0 or iid <= 0 shown)" % n)
    worst = (1.0, None)
    for k in range(0, n+1):
        for l in range(k+1, n+1):
            K = [k, l]; p = max_freq(n, K)
            if p >= 0.5: continue
            gs = gains(n, K, "seq")
            if gs <= 1e-9 and p < worst[0]:
                worst = (p, K); print("  seq-barrier K=%s p=%.4f seq=%+.3e iid=%+.4f" % (K, p, gs, gains(n,K,"iid")), flush=True)
    print("worst two-slice seq-barrier:", worst)
