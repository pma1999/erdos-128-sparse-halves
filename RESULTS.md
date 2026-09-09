# Verified results and open target

Target: for every finite triangle-free graph, a floor(n/2)-set with at most n²/50 edges, or an exhaustively certified strict counterexample. Neither has been obtained.

Best general bound derived here: **2587/100000**, conditional on the published Balogh–Clemen–Lidický max-cut theorem. Rational constants, polynomial identities and finite lemma tests have been recomputed by two independently written verifiers. The scalar optimization has a compiled Lean certificate; the full graph argument does not. No priority is claimed.

- Proof: `outputs/cut-independent.tex`.
- Exact arithmetic: `python outputs/verify-cut-independent.py` and `python outputs/verify-independent.py` (the second was written without reusing the first; both use exact arithmetic only).
- Literature audit and attribution evidence: `LITERATURE.md`.
- Dependency: Balogh–Clemen–Lidický, **Theorem 2(a)**, stated there for *n* large enough; the hypothesis is discharged by the blow-up proposition in the paper.

## What is new here and what is not — corrected 2026-09-09

An earlier version of this file described the contribution as "extending Razborov's Section 4.5 to independence ratio 1/3". **That overstated it.** Reading Section 4.5 in full establishes:

- the branch α ≥ 3/8 of the envelope is Razborov's Theorem 3.6 verbatim;
- his Case 2 already works for every α ≥ 1/3 with no modification — the condition he actually uses is ∂Q₁/∂p_b = (1−3α)/2 ≤ 0, and he assumes 3/8 only for Case 1;
- the extension therefore amounts to one line of his Case 1: for α < 3/8 evaluate the concave quadratic at its interior maximum p_b = 3/4 − α instead of substituting p_b := α.

The actual new step is in Section 3 of the paper: apply the max-cut theorem, delete the edges inside the smaller side so that side becomes independent, apply the completion bound to the modified graph, and pay the deleted density. Razborov cites Balogh–Clemen–Lidický but does not combine it with his Theorem 3.6; Sarid combines the same max-cut theorem with a flag-algebra C₄ bound instead. Nothing found in the sources states this combination.

Being elementary is part of the point: this bound beats a flag-algebra result without any semidefinite certificate, and is therefore within reach of full formalization.

## Ceiling of the route

The supremum over c of the bound is 0.0258691…, so 2587/100000 is this argument's own optimum rounded up. Substituting a perfect max-cut input (1/25, the Erdős conjecture for D₂) would give only ≈ 0.02481. **The 1/50 target is unreachable by this route** without a new ingredient.

Formal scalar certificate: `formal/Scalar.lean`, Lean 4.33.1, 17 theorems compiled and replayed by Lean's kernel. Run `python formal/verify.py`. No unfinished proofs or added mathematical axioms; only `propext`, `Classical.choice`, `Quot.sound`. `scalar_envelope` takes scalar bounds as hypotheses and proves beta < 2587/100000. It does not claim those hypotheses for graphs.

Previous baseline: 13083/500000, banked in commit `e52b279`; proof and verifier retained for comparison. That earlier argument additionally uses Sarid's cubic lemma and C4 certificate and the neighborhood anchor inequality.

Restricted results: the cubelike argument covers orders at most 128 and balanced blow-ups. Exact Clebsch calculations and local-search obstructions are in `outputs/`. They are not counterexamples.

Search: 722342 weighted-template evaluations found no strict counterexample; this is not exhaustive over graph orders or templates. The n=24 SAT search returned unknown, not UNSAT.

Final deliverables not achieved: the 1/50 theorem or counterexample, formal certification of the graph argument, and specialist review.
