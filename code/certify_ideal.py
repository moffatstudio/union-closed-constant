"""
CERTIFICATION RUN (final result) -- team lead, 2026-09-08.

The lead's analytic fixed point for the f_ideal rank-1 kernel: c** = 0.382885260 at
beta** = 0.189778 (the two-point adversary at x* = 0.690908 and the degenerate adversary
mu = q*delta_1 + (1-q)*delta_eps bind simultaneously there). This script certifies
adversary_min (kernel_game.py) at beta = 0.1897 for c in {0.38284, 0.38288, 0.38292},
m in {4,5,6} atoms/component, with 500 random restarts PLUS kernel_game's own automatic
structured_inits() PLUS explicit exact seeds at both known extremal laws (two-point at
x*=0.690908, and the degenerate law at q=1-c with eps down to 1e-6, both ways round).

Question under test: does ANY adversary law other than these two known types (i.e. with
q strictly inside (0,1) AND >=2 effective atoms carrying real weight, or otherwise >=3
total effective atoms) achieve ratio < 1 at these (c, m)? `classify()` labels every
minimiser found as DEGENERATE(known) / TWO-POINT(known) / OTHER so this is answered
directly from the log, not by eyeballing raw atom dumps.

Usage:
    python certify_ideal.py all                  # run the full 3x3 grid, one process
    python certify_ideal.py <c> <m> [restarts]    # run a single cell (for parallel splitting)

Appends every cell to certify_log.txt (human-readable) and certify_results.jsonl (machine).
"""
import sys, time, json
import numpy as np
from kernel_game import make_rank_kernel, adversary_min, unpack, mean_x

BETA_STAR = 0.1897
C_VALUES = [0.38284, 0.38288, 0.38292]
M_VALUES = [4, 5, 6]
RESTARTS = 500
SEED = 1
X_STAR = 0.690908  # lead's reported two-point adversary location at the analytic fixed point


def f_ideal(x):
    x = np.asarray(x, float)
    return np.where(x <= 0.5, np.minimum(x, 1 - x), np.sqrt(np.maximum(0.0, 0.5 - x**2)))


K_IDEAL = make_rank_kernel([f_ideal])


def pad(atoms, wts, m):
    atoms = list(atoms); wts = list(wts)
    while len(atoms) < m:
        atoms.append(atoms[-1] if atoms else 0.0); wts.append(1e-9)
    return np.array(atoms[:m], float), np.array(wts[:m], float)


def build_z(q, atoms0, wts0, atoms1, wts1, m):
    a0, w0 = pad(atoms0, wts0, m); a1, w1 = pad(atoms1, wts1, m)
    w0 = w0 / w0.sum(); w1 = w1 / w1.sum()
    return np.concatenate([[q], w0, a0, w1, a1])


def exact_inits(c, m):
    """The two known extremal laws, seeded exactly (component-swapped and weight-varied)."""
    inits = []
    for p in (0.85, 0.8936, 0.92):
        for q0 in (0.0, 1.0):
            inits.append(build_z(q0, [X_STAR, 0.0], [p, 1 - p], [X_STAR, 0.0], [p, 1 - p], m))
    for eps in (1e-2, 1e-3, 1e-4, 1e-6):
        inits.append(build_z(1 - c, [eps], [1.0], [1.0], [1.0], m))
        inits.append(build_z(c, [1.0], [1.0], [eps], [1.0], m))  # component-swapped
    return inits


def classify(z, m, tol_w=1e-3, tol_x=8e-3):
    q, w0, x0, w1, x1 = unpack(z, m)

    def occupied(atoms, wts):
        idx = np.argsort(atoms)
        atoms, wts = atoms[idx], wts[idx]
        clusters = []
        for a, w in zip(atoms, wts):
            if w < tol_w: continue
            if clusters and abs(a - clusters[-1][0]) < tol_x:
                a0c, w0c = clusters[-1]
                clusters[-1] = ((a0c * w0c + a * w) / (w0c + w), w0c + w)
            else:
                clusters.append((a, w))
        return clusters

    c0 = occupied(x0, w0); c1 = occupied(x1, w1)
    active0 = q < 1 - 1e-4
    active1 = q > 1e-4
    n_active_comp = int(active0) + int(active1)
    is_degenerate = (n_active_comp == 2 and len(c0) == 1 and len(c1) == 1 and
                      ((c0[0][0] < 0.02 and c1[0][0] > 0.98) or (c1[0][0] < 0.02 and c0[0][0] > 0.98)))
    active_clusters = c1 if (active1 and not active0) else (c0 if (active0 and not active1) else None)
    is_two_point = (n_active_comp == 1 and active_clusters is not None and len(active_clusters) == 2 and
                     min(a for a, w in active_clusters) < 0.02)
    n_eff = len(c0) + len(c1)
    label = "DEGENERATE(known)" if is_degenerate else ("TWO-POINT(known)" if is_two_point else "OTHER")
    detail = "q=%.5f | P0 occ=%s | P1 occ=%s" % (
        q, [(round(a, 4), round(w, 4)) for a, w in c0], [(round(a, 4), round(w, 4)) for a, w in c1])
    return label, detail, n_eff


def run_cell(c, m, restarts=RESTARTS, seed=SEED):
    inits = exact_inits(c, m)
    t0 = time.time()
    val, z = adversary_min(K_IDEAL, BETA_STAR, c, m=m, restarts=restarts, seed=seed, inits=inits)
    dt = time.time() - t0
    if z is not None:
        label, detail, neff = classify(z, m)
        mx = mean_x(z, m)
    else:
        label, detail, neff, mx = "NONE", "no feasible point found", 0, -1
    line = ("CERTIFY beta=%.4f c=%.5f m=%d restarts=%d(+%d exact struct) : min_ratio=%.8f mean_x=%.6f "
            "type=%s time=%.0fs\n  %s" % (BETA_STAR, c, m, restarts, len(inits), val, mx, label, dt, detail))
    print(line, flush=True)
    with open("certify_log.txt", "a") as f:
        f.write(line + "\n")
    rec = {"beta": BETA_STAR, "c": c, "m": m, "restarts": restarts, "min_ratio": val, "mean_x": mx,
           "type": label, "detail": detail, "n_effective_atoms": neff, "time_s": dt,
           "z": (z.tolist() if z is not None else None)}
    with open("certify_results.jsonl", "a") as f:
        f.write(json.dumps(rec) + "\n")
    return val, z


if __name__ == "__main__":
    if sys.argv[1] == "all":
        for c in C_VALUES:
            for m in M_VALUES:
                run_cell(c, m)
    else:
        c = float(sys.argv[1]); m = int(sys.argv[2])
        restarts = int(sys.argv[3]) if len(sys.argv) > 3 else RESTARTS
        seed = int(sys.argv[4]) if len(sys.argv) > 4 else SEED
        run_cell(c, m, restarts, seed)
