# Candidate scouting, 2026-09-08 (five Sonnet scouts, state of the art as of Sept 2026)

## Rejected candidates (kept for future campaigns)

### Sidon set constant  |A| <= sqrt(N) + c N^{1/4} + O(1)
- Chain: Lindstrom 1 -> Cilleruelo (2010) -> Balogh-Furedi-Roy 0.998 (2103.15850) -> O'Bryant 0.99703 (2207.07800)
  -> Carter-Hunter-O'Bryant 0.98183 (2310.20032) -> Tao et al. unpublished 0.97633 (tracker teorth.github.io/optimizationproblems C5a)
  -> **Hou-Zhao 0.94349 (arXiv:2607.01169, Jul/Sep 2026)**, "vector-valued smoothing": Hilbert-space Cauchy-Schwarz with an
  8-component kernel/boundary-weight system, certified in exact rationals.
- Modular Z/NZ case: |S|^2-|S|+1 <= n, no N^{1/4} term; the whole term is a boundary artifact.
- Rejected: live race (Tao, Gomez-Serrano, Wagner active), next gain = bigger kernel search.

### Thrackle  |E| <= c|V|
- Chain: LPS 1997 2n-3 -> Cairns-Nikolayevsky 1.5(n-1) -> Fulek-Pach 167/117 (1002.3904) -> Goddyn-Xu 1.4 -> Fulek-Pach 1.3984 (1708.08037)
  -> **Xu 2021 1.393(n-1)** (Appl. Math. Comput. 389, journal-only). Tracker: teorth.github.io/optimizationproblems/constants/78a.html
- Method: discharging + computer enumeration of local configurations; cost explodes as ratio -> 1.
- Rejected: grind for a decimal. Structural lever (Rubinstein dumbbell/theta/figure-eight reduction) is the only interesting angle.

### Lonely runner
- Finite cases proven through n=14 runners (Rosenfeld 2509.14111 n=8; 2512.01912 n=9; Trakulthongchai 2511.22427 n=9,10;
  Sungkawichai-Trakulthongchai 2604.23906 n=11-13; Allikvere 2609.02604 n=14, posted 2026-09-02).
  Enabling result: Malikiosis-Santos-Schymura 2411.06903, speeds <= C(n+1,2)^{n-1}.
- Gap of loneliness: Tao 1701.02048 -> **Bedert 2511.16636: 1/(2n) + 1/n^{5/3+o(1)}** via Riesz products.
- Rejected: compute race (n=15) or deep Fourier analysis (Bedert exponent).

### Opaque set lower bound (unit square)
- Jones 2 -> Kawamura-Moriyama-Otachi-Pach 2.00002 (1403.3894) -> **Kiderlen-Pausinger 2 + 2.3e-5, disc pi + 1.076e-6**
  (2509.08842, Acta Math. Hungar. 2026), using Steinerberger's stability theorem (2501.01004). Kiderlen 2605.13449 = n-dim stability.
- Authors state the local-waste method cannot give bounds better "by magnitudes". Rejected.

## Chosen: union-closed sets constant (Frankl) — see ../../progress.md
- Record 0.38271, Liu arXiv:2306.08824 (June 2023), conditionally-iid coupling, 9-dim numerical optimisation, hypotheses numerically verified.
- Cambie 2212.12500 proved 0.38234 is the exact ceiling of Sawin's mixture-coupling class. Liu's class has NO such ceiling proof.
- Chase-Lovett 2211.11689: psi=(3-sqrt5)/2 is a hard barrier for anything that also handles approximately-union-closed families.
- No citing paper 2024-2026 improves the constant; no AI activity found on it.
- Instructive failure: Scandone 2302.03484 (flaw found by Tao).
