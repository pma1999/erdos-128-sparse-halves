# Research log

## Reconstructed baseline, 2026-09-09

The following experiments were completed before this log was requested. Their saved artifacts are the evidence; this reconstruction does not assert that they were logged contemporaneously.

1. Clebsch exact enumeration: 12870 halves; minimum 4 edges. Verdict: conjecture holds there; standard anchor construction is too weak. See `clebsch-exact-check.json`.
2. Full-neighborhood completion: all such Clebsch halves have at least 6 edges, extending to balanced blow-ups. Verdict: abandon full-neighborhood-only strategies.
3. Cubelike spectral argument: analytic bound N/4 floor(N(3/2-sqrt(2))); suffices through N=128. Tested all 3049 triangle-free generator sets on F2^4 and 300 larger samples. Verdict: restricted result, not universal solution.
4. Exchange barrier: Clebsch blow-ups have a bad half with change at least r(t-r) for an r-exchange. Verdict: fixed-size local improvement can stall.
5. SAT n=24: two 180-second runs, 277 rejected candidates, 4157 cuts. Verdict: UNKNOWN, no exhaustion certificate.
6. Weighted blow-up optimizer: exact subset dynamic programming, checked against exhaustive small instances. Fixed templates 386183 evaluations; joint graph/weight search 336159. Best normalized value 128/6400=1/50. Verdict: no counterexample; end these runs rather than infer truth from heuristics.
7. General perturbation refinement: retain S_x <= mu d_x(1-d_x). Derived 13083/500000 using external max-cut and C4 ingredients. Exact rational constants and 1480 weighted lemma checks pass. Author's C4 verifier also passes. Verdict: partial analytic improvement, no Lean certification or novelty claim.

## Current audit

- Read the objective attachment again. Initialized git in the existing single working directory.
- Opened Sarid's TeX, Razborov's paper, BCL's paper, Norin–Yepremyan's paper, Keevash–Sudakov's paper and the formal-conjectures statement. Searches for 0.026166/0.02616 did not establish an earlier matching bound. This is not an exhaustive novelty audit. The Erdős website requests failed in the web tool; the attachment supplies an older snapshot only.
- Boundary audit: state the strict improved theorem for n>=1; n=0 has the non-strict conclusion with zero edges. Explain Razborov's C4 normalization explicitly.
- New attack: the scalar maximum of the cut bound has e(X)=0. Try an independent-set completion bound after deleting e(X) edges, then pay those edges back. Budget: one derivation and one envelope search; kill criterion: no certified gain or an invalid completion inequality. This is separate from a claim that the full conjecture is solved.
