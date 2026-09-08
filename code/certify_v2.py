"""
CERTIFICATION RUN v2 (final rigor pass) -- team lead correction, 2026-09-08.
beta** = 0.189778 EXACTLY (not the rounded 0.1897 used in certify_ideal.py / the v1 run).

Lead's note: plain adversary_min (SLSQP) cannot resolve the "component-hiding" law, because its
infimum is approached only as some atom's weight -> 0, exactly where ratio()'s `e_h < 1e-12:
return 10.0` guard creates a cliff that repels the optimiser. Three sub-tasks, run separately so
the degenerate family is handled by DIRECT formula evaluation (no optimiser involved at all)
rather than SLSQP:

(1) Degenerate family, direct/closed-form evaluation:
       mu = q*delta_1 + (1-q)*[(1-d)*delta_0 + d*delta_y],   q = 1-c
    d in {1e-2,1e-3,1e-4,1e-6}, y in {0.05,0.2,0.5,0.7}, c = 0.38284.
    Reported via a hand-derived closed form AND kernel_game.ratio() evaluated directly at the
    same point (m=2, no SLSQP) as a cross-check that the closed form is transcribed correctly.

    Closed-form derivation (h(0)=h(1)=0, f_ideal(0)=f_ideal(1)=0 so K(0,*)=K(1,*)=K(*,1)=0):
      qb=1-q=c;  w_b=qb*d (mixture weight on atom y);  w_1=q (mixture weight on atom 1)
      e_h   = qb*d*h(y)                                         [only atom y has h>0]
      e_iid = w_b^2*h(y^2) + 2*w_b*w_1*h(y)                     [pairs not involving atom 0]
      e_K   = qb*d^2*h(y^2 + f_ideal(y)^2)                      [only the (y,y) within-P0 pair]
      ratio = [(1-beta)*e_iid + beta*e_K] / e_h
            = 2*(1-beta)*q + d*[ (1-beta)*qb*h(y^2)/h(y) + beta*h(y^2+f(y)^2)/h(y) ]  + O(d^2)
    so to first order the y-correction is manifestly >= 0 (all terms nonneg): adding this third
    atom can only INCREASE the ratio above the pure d->0 limit 2*(1-beta)*(1-c).

(2) Non-degenerate search with an explicit floor constraint E_mu[h(X)] >= 1e-3 added to
    adversary_min (keeps SLSQP away from the e_h-guard cliff so it explores genuine interior
    laws instead of bouncing off the boundary), m in {4,5,6}, restarts=300 + all structured
    seeds, c in {0.38284, 0.38288}.

(3) Mixed-law grid: combine the two-point law (x*=0.690908, p*~0.8936) and the near-1
    degenerate atom with a small extra mass d at y, in BOTH component-role assignments:
      (a) P0 = (1-d)*[p*delta_{x*} + (1-p)*delta_0] + d*delta_y,   P1 = delta_1
      (b) P0 = p*delta_{x*} + (1-p)*delta_0,                       P1 = (1-d)*delta_1 + d*delta_y
    q in {0.3,0.4,0.5,0.6,0.7}, d in {1e-2,1e-3}, y in {0.05,0.2,0.5,0.7}: direct grid evaluation
    (no optimiser) via kernel_game.ratio(), reporting whether any point dips below the pure-case
    minimum.
"""
import sys, time, json
import numpy as np
from scipy.optimize import minimize
from kernel_game import h, unpack, mean_x, ratio as ratio_fn, make_rank_kernel, structured_inits, describe

BETA = 0.189778
C1, C2 = 0.38284, 0.38288
X_STAR, P_STAR = 0.690908, 0.8936  # lead's two-point law at the analytic fixed point


def f_ideal(x):
    x = np.asarray(x, float)
    return np.where(x <= 0.5, np.minimum(x, 1 - x), np.sqrt(np.maximum(0.0, 0.5 - x**2)))


K_IDEAL = make_rank_kernel([f_ideal])


# ============================================================================
# (1) degenerate family -- direct evaluation, no optimiser
# ============================================================================
def ratio_closed_form(beta, c, d, y):
    q = 1 - c
    qb = c
    fy = f_ideal(np.array([y]))[0]
    hy = h(np.array([y]))[0]
    hy2 = h(np.array([y**2]))[0]
    hK = h(np.array([y**2 + fy**2]))[0]
    num = (1 - beta) * (qb**2 * d**2 * hy2 + 2 * qb * d * q * hy) + beta * qb * d**2 * hK
    den = qb * d * hy
    return num / den


def pad(atoms, wts, m):
    atoms = list(atoms); wts = list(wts)
    while len(atoms) < m:
        atoms.append(atoms[-1] if atoms else 0.0); wts.append(0.0)
    return np.array(atoms[:m], float), np.array(wts[:m], float)


def build_z(qint, atoms0, wts0, atoms1, wts1, m):
    """qint = internal kernel_game q = mixture weight on P1."""
    a0, w0 = pad(atoms0, wts0, m); a1, w1 = pad(atoms1, wts1, m)
    s0, s1 = w0.sum(), w1.sum()
    w0 = w0 / s0 if s0 > 0 else np.ones(m) / m
    w1 = w1 / s1 if s1 > 0 else np.ones(m) / m
    return np.concatenate([[qint], w0, a0, w1, a1])


def part1(beta=BETA, c=C1):
    print("=" * 90)
    print("(1) DEGENERATE FAMILY mu = q*delta_1 + (1-q)*[(1-d)*delta_0 + d*delta_y], q=1-c=%.6f" % (1 - c))
    print("    beta=%.6f  c=%.5f  (base limit 2*(1-beta)*(1-c) = %.7f)" % (beta, c, 2 * (1 - beta) * (1 - c)))
    print("=" * 90)
    results = []
    q_int = 1 - c  # internal kernel_game q = weight on the delta_1 component
    for y in (0.05, 0.2, 0.5, 0.7):
        for d in (1e-2, 1e-3, 1e-4, 1e-6):
            r_closed = ratio_closed_form(beta, c, d, y)
            # cross-check via kernel_game.ratio() directly (m=2, no SLSQP call at all)
            z = build_z(q_int, [0.0, y], [1 - d, d], [1.0, 1.0], [1.0, 0.0], 2)
            r_code = ratio_fn(z, 2, K_IDEAL, beta)
            mx = mean_x(z, 2)
            print("  y=%.2f d=%.0e : ratio_closed=%.8f  ratio_code=%.8f  (match to %.2e)  mean_x=%.7f" %
                  (y, d, r_closed, r_code, abs(r_closed - r_code), mx))
            results.append({"y": y, "d": d, "ratio_closed": r_closed, "ratio_code": r_code, "mean_x": mx})
    print()
    return results


# ============================================================================
# (2) non-degenerate search with an E_mu[h(X)] >= floor constraint
# ============================================================================
def e_h_val(z, m):
    q, w0, x0, w1, x1 = unpack(z, m)
    atoms = np.concatenate([x0, x1]); wts = np.concatenate([(1 - q) * w0, q * w1])
    return wts @ h(atoms)


def adversary_min_floor(K, beta, c, m, restarts, seed, inits=None, floor=1e-3):
    rng = np.random.default_rng(seed)
    bounds = [(0, 1)] * (1 + 4 * m)
    cons = [
        {"type": "ineq", "fun": lambda z: mean_x(z, m) - (1 - c)},
        {"type": "ineq", "fun": lambda z: e_h_val(z, m) - floor},
    ]
    best = (np.inf, None)
    starts = list(inits) if inits is not None else []
    starts += structured_inits(m, rng)
    # exact two-point seed at the analytic optimum
    starts.append(build_z(0.0, [X_STAR, 0.0], [P_STAR, 1 - P_STAR], [X_STAR, 0.0], [P_STAR, 1 - P_STAR], m))
    starts.append(build_z(1.0, [X_STAR, 0.0], [P_STAR, 1 - P_STAR], [X_STAR, 0.0], [P_STAR, 1 - P_STAR], m))
    for _ in range(restarts):
        z0 = rng.random(1 + 4 * m)
        starts.append(z0)
    n_feas0 = 0
    for z0 in starts:
        try:
            r = minimize(ratio_fn, z0, args=(m, K, beta), method="SLSQP", bounds=bounds,
                         constraints=cons, options={"maxiter": 400, "ftol": 1e-13})
        except Exception:
            continue
        if mean_x(r.x, m) < (1 - c) - 1e-9: continue
        if e_h_val(r.x, m) < floor - 1e-9: continue
        n_feas0 += 1
        if r.fun < best[0]: best = (r.fun, r.x)
    return best, len(starts), n_feas0


def part2(c, m, restarts=300, seed=1, floor=1e-3):
    t0 = time.time()
    (val, z), ntot, nfeas = adversary_min_floor(K_IDEAL, BETA, c, m, restarts, seed, floor=floor)
    dt = time.time() - t0
    line = ("(2) FLOOR-SEARCH beta=%.6f c=%.5f m=%d restarts=%d floor=%.0e : "
            "min_ratio=%.8f mean_x=%.6f n_starts=%d n_feasible=%d time=%.0fs" %
            (BETA, c, m, restarts, floor, val, mean_x(z, m) if z is not None else -1, ntot, nfeas, dt))
    print(line, flush=True)
    print("    adversary: %s" % (describe(z, m) if z is not None else None), flush=True)
    with open("certify_v2_log.txt", "a") as f:
        f.write(line + "\n    adversary: %s\n" % (describe(z, m) if z is not None else None))
    rec = {"part": 2, "beta": BETA, "c": c, "m": m, "restarts": restarts, "floor": floor,
           "min_ratio": val, "mean_x": mean_x(z, m) if z is not None else -1,
           "z": z.tolist() if z is not None else None, "time_s": dt}
    with open("certify_v2_results.jsonl", "a") as f:
        f.write(json.dumps(rec) + "\n")
    return val, z


# ============================================================================
# (3) mixed-law grid -- direct evaluation, no optimiser
# ============================================================================
def part3(beta=BETA, c=C1):
    print("=" * 90)
    print("(3) MIXED-LAW GRID (direct evaluation), beta=%.6f c=%.5f" % (beta, c))
    print("=" * 90)
    best = (np.inf, None)
    rows = []
    for q in (0.3, 0.4, 0.5, 0.6, 0.7):
        for d in (1e-2, 1e-3):
            for y in (0.05, 0.2, 0.5, 0.7):
                # (a) hybrid P0 = (1-d)*[p*delta_x* + (1-p)*delta_0] + d*delta_y ; P1 = delta_1
                za = build_z(q, [X_STAR, 0.0, y], [(1 - d) * P_STAR, (1 - d) * (1 - P_STAR), d],
                             [1.0], [1.0], 3)
                ra = ratio_fn(za, 3, K_IDEAL, beta)
                mxa = mean_x(za, 3)
                # (b) P0 = pure two-point ; P1 = (1-d)*delta_1 + d*delta_y
                zb = build_z(q, [X_STAR, 0.0], [P_STAR, 1 - P_STAR],
                             [1.0, y], [1 - d, d], 3)
                rb = ratio_fn(zb, 3, K_IDEAL, beta)
                mxb = mean_x(zb, 3)
                for tag, r, mx, z in (("a", ra, mxa, za), ("b", rb, mxb, zb)):
                    feasible = bool(mx >= (1 - c) - 1e-9)
                    rows.append({"variant": tag, "q": float(q), "d": float(d), "y": float(y),
                                  "ratio": float(r), "mean_x": float(mx), "feasible": feasible})
                    if feasible and r < best[0]:
                        best = (r, (tag, q, d, y))
    print("  scanned %d grid points; min ratio among FEASIBLE points = %.8f  at %s" % (len(rows), best[0], best[1]))
    with open("certify_v2_log.txt", "a") as f:
        f.write("(3) mixed-law grid: min ratio=%.8f at %s\n" % (best[0], best[1]))
    with open("certify_v2_mixed.jsonl", "w") as f:
        for row in rows:
            f.write(json.dumps(row) + "\n")
    print()
    return best, rows


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "part1":
        part1()
    elif mode == "part2":
        c = float(sys.argv[2]); m = int(sys.argv[3])
        restarts = int(sys.argv[4]) if len(sys.argv) > 4 else 300
        part2(c, m, restarts)
    elif mode == "part3":
        part3()
    else:
        raise SystemExit("usage: certify_v2.py {part1|part2 <c> <m> [restarts]|part3}")
