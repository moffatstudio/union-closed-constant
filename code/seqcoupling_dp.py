"""
Exact value of the sequential-coupling entropy game for a given family F on [n].

A, B have marginals uniform on F. A sequential coupling chooses, for every coordinate i and pair of
prefixes (a,b), the joint law of (A_i, B_i) with the prescribed marginals; the only freedom is
s = P(A_i=0, B_i=0 | a,b) in the Frechet interval [max(0,u+v-1), min(u,v)].
The entropy method gives   H(A u B) - H(A) >= G := sum_i E[ h(s_i) - (h(u_i)+h(v_i))/2 ].
This script computes  max over sequential couplings of G  by dynamic programming over prefix pairs.
If G_max > 0 for a union-closed F we have a contradiction, i.e. the method "beats" F.
If G_max <= 0 for a family with max frequency p < 1/2, that family is a barrier for the whole class.

Lead's tool, 2026-09-08.
"""
import math, itertools, sys
from functools import lru_cache

def h(x):
    if x <= 0.0 or x >= 1.0:
        return 0.0
    return -(x*math.log2(x) + (1-x)*math.log2(1-x))

def family_tree(F, n):
    """Return dict prefix(tuple)->(count, u) where u = P(next bit = 0 | prefix) under uniform on F.
    Sets are bitmasks with bit i = element i."""
    cnt = {}
    for S in F:
        for i in range(n+1):
            pref = tuple((S >> j) & 1 for j in range(i))
            cnt[pref] = cnt.get(pref, 0) + 1
    u = {}
    for pref, c in cnt.items():
        if len(pref) < n:
            c0 = cnt.get(pref + (0,), 0)
            u[pref] = c0 / c
    return cnt, u

def max_gain(F, n, grid=None):
    cnt, u = family_tree(F, n)
    u_keys = set(cnt.keys())
    sys.setrecursionlimit(10000)

    @lru_cache(maxsize=None)
    def V(a, b):
        i = len(a)
        if i == n:
            return 0.0
        ua, vb = u[a], u[b]
        lo, hi = max(0.0, ua + vb - 1.0), min(ua, vb)
        base = -0.5*(h(ua) + h(vb))
        # future values
        def fut(s):
            tot = h(s)
            for (x, y, w) in ((0,0,s),(0,1,ua-s),(1,0,vb-s),(1,1,1-ua-vb+s)):
                if w > 1e-12 and (a+(x,)) in u_keys and (b+(y,)) in u_keys:
                    tot += w * V(a+(x,), b+(y,))
            return tot
        if hi - lo < 1e-12:
            return base + fut(lo)
        # concave in s: golden-section search
        gr = (math.sqrt(5)-1)/2
        x1 = hi - gr*(hi-lo); x2 = lo + gr*(hi-lo)
        f1, f2 = fut(x1), fut(x2)
        for _ in range(60):
            if f1 < f2:
                lo = x1; x1 = x2; f1 = f2; x2 = lo + gr*(hi-lo); f2 = fut(x2)
            else:
                hi = x2; x2 = x1; f2 = f1; x1 = hi - gr*(hi-lo); f1 = fut(x1)
        best = max(fut(lo), fut(hi), f1, f2)
        return base + best

    return V((), ())

def iid_gain(F, n):
    cnt, u = family_tree(F, n)
    @lru_cache(maxsize=None)
    def V(a, b):
        i = len(a)
        if i == n: return 0.0
        ua, vb = u[a], u[b]; s = ua*vb
        tot = h(s) - 0.5*(h(ua)+h(vb))
        for (x, y, w) in [(0,0,s),(0,1,ua-s),(1,0,vb-s),(1,1,1-ua-vb+s)]:
            if w > 1e-12 and (a+(x,)) in cnt and (b+(y,)) in cnt: tot += w*V(a+(x,), b+(y,))
        return tot
    return V((), ())

def is_union_closed(F):
    Fs = set(F)
    return all((S | T) in Fs for S in F for T in F)

def max_freq(F, n):
    m = len(F)
    return max(sum((S >> i) & 1 for S in F) for i in range(n)) / m

def entropy_of_union(F, n):
    """Exact H(A u B) for iid uniform A,B, and log2|F|, for reference."""
    m = len(F); cnt = {}
    for S in F:
        for T in F:
            cnt[S|T] = cnt.get(S|T, 0) + 1
    H = -sum((c/m/m)*math.log2(c/m/m) for c in cnt.values())
    return H, math.log2(m)

if __name__ == "__main__":
    # sanity: power set on n elements -> freq 1/2; gain should be <= 0 ... we expect exactly 0 achievable (A=B)
    for n in range(1, 5):
        F = list(range(1 << n))
        print("powerset n=%d freq=%.3f  iid_gain=%.4f  seq_max_gain=%.4f" % (n, max_freq(F,n), iid_gain(F,n), max_gain(F,n)))
    F = [0b000, 0b001, 0b011, 0b101, 0b111]  # union-closed, freq: elem0 in 4/5
    print("uc example", is_union_closed(F), max_freq(F,3), iid_gain(F,3), max_gain(F,3))

def greedy_gain(F, n):
    """Fixed policy: s = point of the Frechet interval closest to 1/2 (max-entropy union coupling)."""
    cnt, u = family_tree(F, n)
    @lru_cache(maxsize=None)
    def V(a, b):
        i = len(a)
        if i == n: return 0.0
        ua, vb = u[a], u[b]
        lo, hi = max(0.0, ua+vb-1.0), min(ua, vb)
        s = min(max(0.5, lo), hi)
        tot = h(s) - 0.5*(h(ua)+h(vb))
        for (x, y, w) in [(0,0,s),(0,1,ua-s),(1,0,vb-s),(1,1,1-ua-vb+s)]:
            if w > 1e-12 and (a+(x,)) in cnt and (b+(y,)) in cnt: tot += w*V(a+(x,), b+(y,))
        return tot
    return V((), ())
