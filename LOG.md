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

## Cut and independent-set envelope, 2026-09-09

- Derived the extension f(alpha)=3 alpha²/2 - 5 alpha/4 + 9/32 on [1/3,3/8] from the completion argument in Razborov Section 4.5. The published branch alpha(1/2-alpha)/2 handles [3/8,1/2].
- Exact audit initially FAILED: my independently expanded second-moment calculation omitted a factor 1/2 in the term -kd/2. Re-derivation identified and repaired that error. It did not alter the proposed f, but the failed version is not a proof.
- Delete internal edges in the smaller cut side X, apply the independent-set envelope, then restore those edges at cost at most q=e(X)/n². Combine with the profile supported on Y. This gives two scalar bounds Ic² and c²(I+f(x))/(1+c²), where x=1-1/(2c).
- Numerical exploration suggested 0.0258692. This was guidance only. The exact interval proof uses c0=7797/10000 and certifies **2587/100000** on the entire interval c in [1/2,1].
- PASS: positive rational margins, polynomial identities, 92 explicit weighted lemma instances (13 in [1/3,3/8)), and exhaustive enumeration of the 440 triangle-free labeled graphs on 0 through 5 vertices. Output: `outputs/cut-independent-verification.json`. No floats in this verifier.
- No compiled Lean formalization exists. No priority or final-solution claim is made. Source searches for 0.02587/0.0259 did not establish a prior matching result, but are not an exhaustive literature audit.
- Opened arXiv:2606.28041, a newer claimed max-cut result. Its certificates have not been audited; it is NOT used as an assumption or added to verified results.
- Verdict: bank the strict partial improvement; stop tuning decimal constants on this line. A stronger structural relation is needed for 1/50.

## Next structural test

Conjectured intermediate statement, NOT proved: if a maximum cut has an independent side X, then e(Y) <= |X|²/4. Test exactly on small weighted templates before investing in a proof. Budget: one bounded search and immediate abandonment on a counterexample. Even if true, this would only address a restricted configuration.

- Initial test: 3000 saturated weighted templates, 3110 qualifying independent-side maximum cuts, no failure. This was a bounded search, not a proof or a valid saturation reduction for the auxiliary claim.
- Unrestricted SAT test immediately returned SAT at n=8, |X|=2. The other side has two internal edges, violating 4e(Y)<=|X|². The saved graph has an independent half and is not a counterexample to Erdős 128.
- Independent verifier enumerates all 256 cuts and all 70 halves. Maximum cut is 8, minimum half cost is 0. An explicit infinite family explains the failure: t paths of length two and t paths of length three between the same two endpoints.
- Verdict: **auxiliary inequality refuted; abandon this line**. Do not incorporate it into the partial-bound proof. Saturation had hidden these examples by changing the maximizing partitions.

## Lean scalar certification, 2026-09-09

- Goal: certify the algebraic part of the banked argument before attempting a full formal graph construction. Budget: portable runtime plus one scalar module; no theorem about graphs will be asserted from scalar tests.
- Consulted the context7 skill and official Lean documentation/source. Installed portable Lean 4.33.1 solely within work/lean-runtime. Official archive SHA-256: c39360867edfff6b090f20c16e18581c969ce839b71e813d76022ec04ec73e4d. No elan, global configuration, or Mathlib installation.
- Initial ordinary decide calls failed because Rat arithmetic definitions are marked irreducible. Replaced them with kernel reduction (`decide +kernel`), not native_decide. Initial broad grind calls caused excessive kernel recursion; replaced them with smaller explicit algebra/order lemmas. Failed compilations were never accepted as certificates.
- A leanchecker --help probe did not behave as a help command; source inspection showed it defaults to replaying project modules when no target is supplied. The probe was canceled. The final verification names Scalar explicitly and completed successfully.
- PASS: 17 Lean theorems covering exact constants, three polynomial completion identities, three interval inequalities, and their conditional scalar envelope. All theorem dependency lists contain only propext, Classical.choice and Quot.sound; no sorryAx, generated error axioms, native-decide axioms or added mathematical axioms.
- PASS: formal/verify.py recompiles the module and replays its declarations in Lean's kernel against the imported Std library. Output: outputs/lean-scalar-verification.json. This is not an external checker and does not reprove Std from scratch.
- Verdict: scalar certification achieved. The coefficient remains 2587/100000; there is no new numerical bound in this turn. The graph construction, rounding, and BCL theorem are not formalized. The 1/50 target remains unresolved.
