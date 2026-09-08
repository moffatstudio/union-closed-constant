"""
Robustness sweep for the f_ideal rank-1 kernel candidate (task from team lead, 2026-09-08).
f_ideal(x) = min(x,1-x) for x<=1/2; sqrt(max(0, 1/2-x^2)) for x>1/2  (0 for x>=1/sqrt2).
Claim under test: with beta=0.15, c_max=0.382840 at m=3 atoms/component (see sweep_ideal_b0.15.log).
This script re-runs adversary_min at m in {4,5,6}, for beta in {0.15,0.20} and c in
{0.38280, 0.38284, 0.38290}, with >=300 random restarts PLUS a battery of structured
initial guesses (two-point laws, Cambie's law, Liu's law, 3-atom laws), and reports the
minimum ratio and minimiser found for each (beta, c, m).

Usage: python robustness_ideal.py <beta> <c> <m> [restarts] [seed]
Prints one result line + adversary description; appends to robustness_results.jsonl.
"""
import sys, time, json
import numpy as np
from kernel_game import make_rank_kernel, adversary_min, describe, unpack, mean_x

def f_ideal(x):
    x = np.asarray(x, float)
    return np.where(x <= 0.5, np.minimum(x, 1 - x), np.sqrt(np.maximum(0.0, 0.5 - x**2)))

K_IDEAL = make_rank_kernel([f_ideal])

# Liu's exact reported optimum (liu_reproduce.py, eqs 87-88): q=0, P0 = p*delta_{x*} + (1-p*)delta_0
LIU_P, LIU_X = 0.893604513905457, 0.690787593924988
# Yu/Cambie near-optimal Sawin-mixture MARGINAL law (arXiv:2212.00658 / Cambie's refinement): the marginal
# of Q_{a,a}/Q_{a,1} mixture is a two-point law on {a, 1} with weights (1-beta, beta).
CAMBIE_A, CAMBIE_BETA = 0.3300622, 0.1560676

def pad(atoms, wts, m):
    atoms = list(atoms); wts = list(wts)
    while len(atoms) < m:
        atoms.append(atoms[-1] if atoms else 0.0)
        wts.append(1e-9)
    return np.array(atoms[:m], float), np.array(wts[:m], float)

def build_z(q, atoms0, wts0, atoms1, wts1, m):
    a0, w0 = pad(atoms0, wts0, m); a1, w1 = pad(atoms1, wts1, m)
    w0 = w0 / w0.sum(); w1 = w1 / w1.sum()
    return np.concatenate([[q], w0, a0, w1, a1])

def structured_inits(m):
    inits = []
    for xstar in np.linspace(0.60, 0.75, 16):
        for q0 in (0.0, 1.0):
            inits.append(build_z(q0, [xstar, 0.0], [0.9, 0.1], [xstar, 0.0], [0.9, 0.1], m))
    # Cambie's law (marginal two-point law on {a,1}); tried as both P0 and as P1 (q=0/q=1)
    for q0 in (0.0, 1.0):
        inits.append(build_z(q0, [CAMBIE_A, 1.0], [1 - CAMBIE_BETA, CAMBIE_BETA],
                              [CAMBIE_A, 1.0], [1 - CAMBIE_BETA, CAMBIE_BETA], m))
    # Liu's law
    for q0 in (0.0, 1.0):
        inits.append(build_z(q0, [LIU_X, 0.0], [LIU_P, 1 - LIU_P], [LIU_X, 0.0], [LIU_P, 1 - LIU_P], m))
    # 3-atom laws with atoms spread in [0, 0.75]
    rng = np.random.default_rng(12345)
    grids = [[0.0, 0.375, 0.75], [0.0, 0.25, 0.65], [0.1, 0.4, 0.7],
             [0.0, 0.5, 0.75], [0.2, 0.45, 0.7], [0.05, 0.35, 0.75]]
    for atoms3 in grids:
        for _ in range(4):
            w = rng.dirichlet(np.ones(3))
            inits.append(build_z(0.0, atoms3, w, atoms3, w, m))
    return inits

def run(beta, c, m, restarts, seed):
    inits = structured_inits(m)
    t0 = time.time()
    val, z = adversary_min(K_IDEAL, beta, c, m=m, restarts=restarts, seed=seed, inits=inits)
    dt = time.time() - t0
    return val, z, dt, len(inits)

if __name__ == "__main__":
    beta = float(sys.argv[1]); c = float(sys.argv[2]); m = int(sys.argv[3])
    restarts = int(sys.argv[4]) if len(sys.argv) > 4 else 300
    seed = int(sys.argv[5]) if len(sys.argv) > 5 else 1
    val, z, dt, ninit = run(beta, c, m, restarts, seed)
    mx = mean_x(z, m) if z is not None else -1
    print("RESULT beta=%.2f c=%.5f m=%d restarts=%d(+%d struct) : min_ratio=%.8f mean_x=%.6f time=%.0fs" %
          (beta, c, m, restarts, ninit, val, mx, dt), flush=True)
    print("  adversary: %s" % (describe(z, m) if z is not None else None), flush=True)
    rec = {"beta": beta, "c": c, "m": m, "restarts": restarts, "n_struct_inits": ninit,
           "min_ratio": val, "mean_x": mx, "time_s": dt,
           "z": (z.tolist() if z is not None else None)}
    with open("robustness_results.jsonl", "a") as f:
        f.write(json.dumps(rec) + "\n")
