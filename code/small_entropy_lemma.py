"""Small-entropy lemma check. NOTE (referee, round 2): the printed bound (1) is for the pure iid ratio; the mixture ratio R gets the extra factor w = 0.810222, i.e. 0.849 -- NOT above C. Kept for the record; the lemma is asymptotic only.
  ratio >= 2*kappa(eta) * (1 - c - eta - E_mu h(X)/h(eta)),  kappa(eta) = (1-eta)(1 - 2/log2(1/eta)),  any eta in (0,1/4].
(1) Evaluate the bound at eta = 1e-4 for E h <= 1e-7 and c = 0.38284.
(2) Brute-force check: random laws with small entropy; verify the IID ratio E h(XY)/E h(X) >= bound for many eta.
(3) Floor search at floor 1e-7 (m=4) for the mixture certificate."""
import numpy as np, time
from kernel_game import h as hnat

def hb(x):
    x = np.clip(x, 1e-300, 1 - 1e-16)
    return -(x * np.log2(x) + (1 - x) * np.log2(1 - x))

def kappa(eta): return (1 - eta) * (1 - 2 / np.log2(1 / eta))

c = 0.38284
print("(1) bound at eta=1e-4, E h <= 1e-7:", 2 * kappa(1e-4) * (1 - c - 1e-4 - 1e-7 / hb(1e-4)))
print("    bound at eta=1e-5, E h <= 1e-8:", 2 * kappa(1e-5) * (1 - c - 1e-5 - 1e-8 / hb(1e-5)))

rng = np.random.default_rng(0); worst = np.inf
for trial in range(20000):
    k = rng.integers(2, 6)
    # atoms: mostly at 0/1 with small perturbations, plus a few interior atoms with tiny weight
    xs = np.concatenate([rng.choice([0.0, 1.0], size=k) + rng.uniform(-1, 1, size=k) * 10.0 ** rng.uniform(-9, -2, size=k), rng.uniform(0, 1, size=2)])
    xs = np.clip(xs, 0, 1)
    ws = np.concatenate([rng.dirichlet(np.ones(k)), 10.0 ** rng.uniform(-9, -3, size=2)]); ws /= ws.sum()
    mean = ws @ xs
    if mean < 1 - c: continue
    Eh = ws @ hb(xs)
    if Eh <= 0 or Eh > 1e-3: continue
    ratio = ws @ hb(np.outer(xs, xs)) @ ws / Eh
    for eta in (1e-2, 1e-3, 1e-4, 1e-5):
        bnd = 2 * kappa(eta) * (1 - c - eta - Eh / hb(eta))
        worst = min(worst, ratio - bnd)
        if ratio < bnd - 1e-12:
            print("VIOLATION", eta, ratio, bnd, xs, ws); break
print("(2) brute-force: min(ratio - bound) over trials =", worst, "(non-negative means the lemma held on every sample)")

# (3) floor 1e-7 search
from floor_scan import search, e_h, describe, m
t0 = time.time(); val, z = search(1e-7, restarts=150, seed=23)
print("(3) floor=1e-7 : min ratio=%.8f  E_h=%.2e  %s  (%.0fs)" % (val, e_h(z), describe(z, m), time.time() - t0))
